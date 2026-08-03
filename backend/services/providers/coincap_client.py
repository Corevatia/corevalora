import requests

from core.errors import UpstreamTimeout, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream


class CoinCapClient:
    def __init__(self, api_key):
        self.baseurl = "https://rest.coincap.io"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _get(self, url: str, params: dict | None = None) -> dict:
        try:
            r = self.session.get(url, params=params, timeout=2)
        except requests.Timeout as e:
            raise UpstreamTimeout(f"CoinCap timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"CoinCap unreachable: {url}") from e

        raise_for_upstream(r)

        return r.json()

    def get_asset(self, asset_id: str) -> dict:
        return self._get(f"{self.baseurl}/v3/assets/{asset_id}")

    def get_assets(self, asset_ids: list[str]) -> dict:
        return self._get(f"{self.baseurl}/v3/assets", {"ids": ",".join(asset_ids)})

    def search_assets(self, query: str) -> dict:
        return self._get(f"{self.baseurl}/v3/assets", {"search": query})
