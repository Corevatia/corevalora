from datetime import UTC, date, datetime, timedelta

import pytest

from core.config import settings
from core.errors import AssetNotFound, UpstreamUnavailable
from db.models import AssetPriceCache
from services import metal_service
from services.cache.price_cache import CACHE_TTL_SECONDS, read_price


class FakeClient:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = 0

    def get_latest_metals(self):
        self.calls += 1
        if self.error:
            raise self.error
        return self.response


def latest_response():
    return {
        "status": "success",
        "currency": "USD",
        "unit": "g",
        "metals": {"gold": 130.0, "silver": 1.5, "platinum": 40.0, "palladium": 35.0},
        "timestamps": {"metal": "2026-08-30T14:00:00.000Z"},
    }


def cache_row(age_seconds):
    return AssetPriceCache(
        kind="metal",
        key="gold",
        symbol="Au",
        asset_name="Gold",
        price=130,
        currency="USD",
        price_date=date(2026, 8, 30),
        cached_at=datetime.now(UTC) - timedelta(seconds=age_seconds),
    )


@pytest.fixture
def fake_client(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_DATA", False)

    def install(**kwargs):
        client = FakeClient(**kwargs)
        monkeypatch.setattr(metal_service, "client", client)
        return client

    return install


def test_unknown_metal_is_rejected_before_the_upstream_call(db, fake_client):
    client = fake_client(response=latest_response())

    with pytest.raises(AssetNotFound):
        metal_service.get_price("copper", db)

    assert client.calls == 0


def test_fresh_cache_is_served_without_an_upstream_call(db, fake_client):
    db.add(cache_row(age_seconds=0))
    db.flush()
    client = fake_client(response=latest_response())

    result = metal_service.get_price("gold", db)

    assert result.price == 130.0
    assert result.stale is False
    assert client.calls == 0


def test_one_upstream_call_caches_every_supported_metal(db, fake_client):
    client = fake_client(response=latest_response())

    result = metal_service.get_price("gold", db)

    assert result.price == 130.0
    assert result.date == "2026-08-30"
    assert result.stale is False
    assert client.calls == 1

    cached = {
        key: read_price(db, kind="metal", key=key)
        for key in metal_service.SUPPORTED_METALS
    }
    assert all(row is not None for row in cached.values())
    assert cached["silver"].price == 1.5
    assert cached["silver"].symbol == "Ag"


def test_upstream_error_with_cache_serves_stale(db, fake_client):
    db.add(cache_row(age_seconds=CACHE_TTL_SECONDS["metal"] + 60))
    db.flush()
    fake_client(error=UpstreamUnavailable("/v1/latest -> 500"))

    result = metal_service.get_price("gold", db)

    assert result.price == 130.0
    assert result.date == "2026-08-30"
    assert result.stale is True


def test_upstream_error_without_cache_raises(db, fake_client):
    fake_client(error=UpstreamUnavailable("/v1/latest -> 500"))

    with pytest.raises(UpstreamUnavailable):
        metal_service.get_price("gold", db)


def test_supported_metals_are_listed():
    listed = metal_service.get_supported_metals()

    assert {m.key for m in listed} == set(metal_service.SUPPORTED_METALS)
