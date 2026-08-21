from datetime import date, timedelta

from sqlalchemy import select

from db.models import Holding, Transaction
from models.crypto import Crypto
from services import crypto_service


def fake_get_crypto_price(asset_id, db):
    return Crypto(
        key=asset_id,
        symbol="FAKE",
        name="Fake Asset",
        price=100.0,
        currency="USD",
        date="2026-07-16",
    )


def payload(**overrides):
    body = {
        "asset": "Solana",
        "key": "solana",
        "symbol": "SOL",
        "kind": "crypto",
        "side": "buy",
        "amount": 10,
        "price": 150,
        "traded_on": "2026-02-01",
    }
    body.update(overrides)
    return body


def btc(**overrides):
    return payload(asset="Bitcoin", key="bitcoin", symbol="BTC", **overrides)


def all_transactions(db):
    return db.execute(select(Transaction)).scalars().all()


def test_buy_creates_position_and_transaction(auth_client, db, user, monkeypatch):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    resp = auth_client.post("/portfolio/transactions", json=payload())

    assert resp.status_code == 201
    assert resp.json()["amount"] == 10
    assert resp.json()["avg_price"] == 150

    holding = db.execute(
        select(Holding).where(Holding.user_id == user.id, Holding.key == "solana")
    ).scalar_one()
    tx = holding.transactions[0]
    assert len(holding.transactions) == 1
    assert (tx.side, tx.amount, tx.price) == ("buy", 10, 150)
    assert tx.traded_on == date(2026, 2, 1)


def test_second_buy_reuses_the_position(auth_client, db, holding, monkeypatch):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    resp = auth_client.post(
        "/portfolio/transactions", json=btc(amount=2.5, price=60000)
    )

    assert resp.status_code == 201
    assert resp.json()["id"] == holding.id
    assert resp.json()["amount"] == 5
    assert resp.json()["avg_price"] == 50000
    assert len(db.execute(select(Holding)).scalars().all()) == 1
    assert len(all_transactions(db)) == 2


def test_future_trade_date_is_rejected(auth_client, db):
    tomorrow = date.today() + timedelta(days=1)

    resp = auth_client.post(
        "/portfolio/transactions", json=payload(traded_on=tomorrow.isoformat())
    )

    assert resp.status_code == 422
    assert all_transactions(db) == []


def test_today_is_accepted(auth_client, monkeypatch):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    resp = auth_client.post(
        "/portfolio/transactions", json=payload(traded_on=date.today().isoformat())
    )

    assert resp.status_code == 201


def test_sell_shrinks_the_amount_but_keeps_the_avg_price(
    auth_client, db, holding, monkeypatch
):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    resp = auth_client.post("/portfolio/transactions", json=btc(side="sell", amount=1))

    assert resp.status_code == 201
    assert resp.json()["amount"] == 1.5
    assert resp.json()["avg_price"] == 40000
    assert len(all_transactions(db)) == 2


def test_selling_more_than_held_is_a_conflict(auth_client, db, holding):
    resp = auth_client.post("/portfolio/transactions", json=btc(side="sell", amount=3))

    assert resp.status_code == 409
    assert len(all_transactions(db)) == 1


def test_selling_an_asset_that_is_not_held_is_a_conflict(auth_client, db):
    resp = auth_client.post("/portfolio/transactions", json=payload(side="sell"))

    assert resp.status_code == 409
    assert db.execute(select(Holding)).scalars().all() == []


def test_backdated_sell_must_be_covered_on_its_own_date(
    auth_client, db, holding, monkeypatch
):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)
    auth_client.post(
        "/portfolio/transactions",
        json=btc(amount=5, price=60000, traded_on="2026-03-01"),
    )

    # 7.5 held today, but only 2.5 on the day this sell claims to have happened.
    resp = auth_client.post(
        "/portfolio/transactions",
        json=btc(side="sell", amount=4, traded_on="2026-02-01"),
    )

    assert resp.status_code == 409
    assert len(all_transactions(db)) == 2


def test_position_sold_off_keeps_its_history_but_leaves_the_portfolio(
    auth_client, db, holding, monkeypatch
):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    sold = auth_client.post(
        "/portfolio/transactions", json=btc(side="sell", amount=2.5)
    )
    listed = auth_client.get("/portfolio/holdings")

    assert sold.status_code == 201
    assert sold.json()["amount"] == 0
    assert listed.json() == []
    assert db.get(Holding, holding.id) is not None
    assert len(all_transactions(db)) == 2


def test_history_is_newest_first(auth_client, holding, monkeypatch):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)
    auth_client.post(
        "/portfolio/transactions",
        json=btc(amount=1, price=50000, traded_on="2026-03-01"),
    )

    resp = auth_client.get(f"/portfolio/holdings/{holding.id}/transactions")

    assert resp.status_code == 200
    assert [tx["traded_on"] for tx in resp.json()] == ["2026-03-01", "2026-01-15"]
    assert resp.json()[0]["side"] == "buy"
    assert resp.json()[0]["amount"] == 1


def test_history_of_another_users_holding_is_not_found(auth_client, other_holding):
    resp = auth_client.get(f"/portfolio/holdings/{other_holding.id}/transactions")

    assert resp.status_code == 404


def test_deleting_a_transaction_updates_the_position(
    auth_client, db, holding, monkeypatch
):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)
    added = auth_client.post(
        "/portfolio/transactions", json=btc(amount=2.5, price=60000)
    )
    assert added.json()["avg_price"] == 50000

    history = auth_client.get(f"/portfolio/holdings/{holding.id}/transactions").json()
    resp = auth_client.delete(f"/portfolio/transactions/{history[0]['id']}")
    listed = auth_client.get("/portfolio/holdings").json()

    assert resp.status_code == 204
    assert listed[0]["amount"] == 2.5
    assert listed[0]["avg_price"] == 40000
    assert len(all_transactions(db)) == 1


def test_deleting_a_buy_that_covers_a_sell_is_a_conflict(
    auth_client, db, holding, monkeypatch
):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)
    auth_client.post("/portfolio/transactions", json=btc(side="sell", amount=2))
    buy_id = holding.transactions[0].id

    resp = auth_client.delete(f"/portfolio/transactions/{buy_id}")

    assert resp.status_code == 409
    assert db.get(Transaction, buy_id) is not None


def test_deleting_another_users_transaction_is_not_found(
    auth_client, db, other_holding
):
    foreign_id = other_holding.transactions[0].id

    resp = auth_client.delete(f"/portfolio/transactions/{foreign_id}")

    assert resp.status_code == 404
    assert db.get(Transaction, foreign_id) is not None


def test_transactions_without_session_is_unauthorized(client):
    resp = client.post("/portfolio/transactions", json=payload())

    assert resp.status_code == 401
