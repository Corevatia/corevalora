from datetime import UTC, datetime, timedelta

import pytest

from core.config import settings
from core.errors import AssetNotFound, UpstreamUnavailable
from db.models import AssetPriceCache
from services import crypto_service
from services.cache.price_cache import CACHE_TTL_SECONDS


class FakeClient:
    def __init__(self, error):
        self.error = error

    def get_asset(self, asset_id):
        raise self.error


def stale_cache_row():
    return AssetPriceCache(
        kind="crypto",
        key="bitcoin",
        symbol="BTC",
        asset_name="Bitcoin",
        price=60000.0,
        currency="USD",
        cached_at=datetime.now(UTC)
        - timedelta(seconds=CACHE_TTL_SECONDS["crypto"] + 60),
    )


def test_upstream_error_with_cache_serves_stale(db, monkeypatch):
    db.add(stale_cache_row())
    db.flush()
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(
        crypto_service, "client", FakeClient(UpstreamUnavailable("/v3/assets -> 500"))
    )

    result = crypto_service.get_crypto_price("bitcoin", db)

    assert result.price == 60000.0
    assert result.stale is True


def test_upstream_error_without_cache_raises(db, monkeypatch):
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(
        crypto_service, "client", FakeClient(UpstreamUnavailable("/v3/assets -> 500"))
    )

    with pytest.raises(UpstreamUnavailable):
        crypto_service.get_crypto_price("bitcoin", db)


def test_unknown_asset_never_serves_stale_cache(db, monkeypatch):
    db.add(stale_cache_row())
    db.flush()
    monkeypatch.setattr(settings, "MOCK_DATA", False)
    monkeypatch.setattr(
        crypto_service, "client", FakeClient(AssetNotFound("/v3/assets -> 404"))
    )

    with pytest.raises(AssetNotFound):
        crypto_service.get_crypto_price("bitcoin", db)
