import pytest

from core.errors import AssetNotFound, UpstreamUnavailable
from services import crypto_service, portfolio_service


def raise_on_price(error):
    def _raise(asset_id, db):
        raise error

    return _raise


def test_upstream_error_degrades_the_holding(db, user, holding, monkeypatch):
    monkeypatch.setattr(
        crypto_service,
        "get_price",
        raise_on_price(UpstreamUnavailable("/v3/assets -> 503")),
    )

    result = portfolio_service.list_holdings(user, db)

    assert len(result) == 1
    assert result[0].id == holding.id
    assert result[0].price is None
    assert result[0].stale is True
    assert result[0].amount == 2.5
    assert result[0].avg_price == 40000


def test_delisted_asset_degrades_the_holding(db, user, holding, monkeypatch):
    monkeypatch.setattr(
        crypto_service, "get_price", raise_on_price(AssetNotFound("bitcoin"))
    )

    result = portfolio_service.list_holdings(user, db)

    assert len(result) == 1
    assert result[0].price is None
    assert result[0].stale is True


def test_bug_while_pricing_is_not_swallowed(db, user, holding, monkeypatch):
    monkeypatch.setattr(
        crypto_service, "get_price", raise_on_price(KeyError("priceUsd"))
    )

    with pytest.raises(KeyError):
        portfolio_service.list_holdings(user, db)
