import pytest

from core.errors import AssetNotFound, ProviderRejected, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream

URL_WITH_KEY = "https://api.marketstack.com/v2/eod?symbols=AAPL&access_key=secret123"


class FakeResponse:
    def __init__(self, status_code, url=URL_WITH_KEY, text=""):
        self.status_code = status_code
        self.url = url
        self.text = text
        self.ok = status_code < 400


def test_success_does_not_raise():
    raise_for_upstream(FakeResponse(200))


@pytest.mark.parametrize(
    ("status_code", "expected_error"),
    [
        (404, AssetNotFound),
        (422, ProviderRejected),
        (429, UpstreamUnavailable),
        (500, UpstreamUnavailable),
    ],
)
def test_status_maps_to_error(status_code, expected_error):
    with pytest.raises(expected_error):
        raise_for_upstream(FakeResponse(status_code))


def test_api_key_does_not_reach_the_error_message():
    with pytest.raises(UpstreamUnavailable) as excinfo:
        raise_for_upstream(FakeResponse(500))

    assert "secret123" not in str(excinfo.value)
    assert "/v2/eod" in str(excinfo.value)
