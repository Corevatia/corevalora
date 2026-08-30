import pytest

from core.config import settings
from core.errors import (
    AssetNotFound,
    ProviderRejected,
    UpstreamTimeout,
    UpstreamUnavailable,
)
from services import crypto_service


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (AssetNotFound("unknown-coin"), 404),
        (UpstreamTimeout("CoinCap timeout"), 504),
        (UpstreamUnavailable("/v3/assets -> 500"), 503),
        (ProviderRejected("/v3/assets -> 422"), 503),
    ],
)
def test_service_error_maps_to_status(auth_client, monkeypatch, error, expected_status):
    def raise_error(asset_id, db):
        raise error

    monkeypatch.setattr(crypto_service, "get_price", raise_error)

    resp = auth_client.get("/crypto/price/bitcoin")

    assert resp.status_code == expected_status
    assert resp.json()["detail"]


def test_unknown_currency_returns_404(auth_client, monkeypatch):
    monkeypatch.setattr(settings, "MOCK_DATA", True)

    resp = auth_client.get("/currency/rates/XXX")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Currency not found"


def test_known_currency_returns_rates(auth_client, monkeypatch):
    monkeypatch.setattr(settings, "MOCK_DATA", True)

    resp = auth_client.get("/currency/rates/CHF")

    assert resp.status_code == 200
    assert resp.json()["base_currency"] == "CHF"
