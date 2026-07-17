from db.models import Holding
from models.crypto import Crypto
from services import crypto_service


def fake_get_crypto_price(asset_id, db):
    return Crypto(
        key=asset_id,
        symbol="FAKE",
        name="Fake Asset",
        price=100.0,
        currency="USD",
        date="2026-07-16"
    )

def test_holdings_returns_only_own_holdings(auth_client, holding, other_holding, monkeypatch):
    monkeypatch.setattr(crypto_service, "get_crypto_price", fake_get_crypto_price)

    resp = auth_client.get("/portfolio/holdings")

    assert resp.status_code == 200
    assert [h["id"] for h in resp.json()] == [holding.id]
    assert resp.json()[0]["price"] == 100

def test_delete_other_user_holding_is_not_found(auth_client, holding, other_holding, db):
    resp = auth_client.delete(f'/portfolio/holdings/{other_holding.id}')

    assert resp.status_code == 404
    assert db.get(Holding, other_holding.id) is not None

def test_portfolio_without_session_is_unauthorized(client):
    get = client.get('/portfolio/holdings')
    post = client.post('/portfolio/holdings', json={
        'asset': 'Bitcoin',
        'key': 'bitcoin',
        'symbol': 'BTC',
        'amount': 1.0,
        'buy_price': 100,
        'kind': 'crypto',
    })
    delete = client.delete('/portfolio/holdings/0')

    assert get.status_code == 401
    assert post.status_code == 401
    assert delete.status_code == 401
