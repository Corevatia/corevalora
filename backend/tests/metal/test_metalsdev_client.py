import pytest

from core.errors import AssetNotFound, ProviderRejected, UpstreamUnavailable
from services.providers.metalsdev_client import (
    MetalsDevClient,
    raise_for_metals_status,
)

WHERE = "/v1/latest"


def test_success_does_not_raise():
    raise_for_metals_status({"status": "success", "metals": {"gold": 130.0}}, WHERE)


@pytest.mark.parametrize(
    "body",
    [
        {
            "status": "failure",
            "error_message": "The API Key provided is invalid.",
            "error_code": 1101,
        },
        {"status": "success"},
        {},
    ],
)
def test_failure_in_a_200_body_raises(body):
    with pytest.raises(UpstreamUnavailable):
        raise_for_metals_status(body, WHERE)


def test_failure_error_code_1203_is_provider_rejected():
    body = {
        "status": "failure",
        "error_message": "	The quota for the current is exceeded.",
        "error_code": 1203,
    }
    with pytest.raises(ProviderRejected):
        raise_for_metals_status(body, WHERE)


def test_error_message_reaches_the_exception():
    body = {"status": "failure", "error_message": "invalid api key", "error_code": 1101}

    with pytest.raises(UpstreamUnavailable) as excinfo:
        raise_for_metals_status(body, WHERE)

    assert "invalid api key" in str(excinfo.value)


def test_a_404_on_the_batch_endpoint_is_not_an_asset_error(monkeypatch):
    client = MetalsDevClient(api_key="dummy")

    def raise_not_found(url, params):
        raise AssetNotFound(f"{WHERE} -> 404")

    monkeypatch.setattr(client, "_get", raise_not_found)

    with pytest.raises(UpstreamUnavailable):
        client.get_latest_metals()
