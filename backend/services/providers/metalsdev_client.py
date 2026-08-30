import requests

from core.errors import UpstreamTimeout, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream


class MetalsDevClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.metals.dev"
        self.api_key = api_key

    def _get(self, url: str, params: dict) -> dict:
        try:
            r = self.session.get(
                url, params={**params, "api_key": self.api_key}, timeout=5
            )
        except requests.Timeout as e:
            raise UpstreamTimeout(f"Metals.Dev timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"Metals.Dev unreachable: {url}") from e

        raise_for_upstream(r)
        return r.json()

    def get_latest_metals(self) -> dict:
        return self._get(f"{self.baseurl}/v1/latest", {"unit": "g", "currency": "USD"})
