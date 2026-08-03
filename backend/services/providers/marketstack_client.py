import requests

from core.errors import UpstreamTimeout, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream


class MarketStackClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.marketstack.com"
        self.api_key = api_key

    def _get(self, url: str, params: dict) -> dict:
        try:
            r = self.session.get(
                url, params={**params, "access_key": self.api_key}, timeout=5
            )
        except requests.Timeout as e:
            raise UpstreamTimeout(f"MarketStack timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"MarketStack unreachable: {url}") from e

        raise_for_upstream(r)
        return r.json()

    def search_tickers(self, query: str) -> dict:
        return self._get(f"{self.baseurl}/v2/tickerslist", {"search": query})

    def get_asset_eod(self, symbol: str) -> dict:
        return self._get(f"{self.baseurl}/v2/eod", {"symbols": symbol})

    # Backup (Marketstack v1)
    def search_tickers_backup(self, query: str) -> dict:
        return self._get(f"{self.baseurl}/v1/tickers", {"search": query})

    def get_asset_price_backup(self, symbol: str) -> dict:
        return self._get(f"{self.baseurl}/v1/eod", {"symbols": symbol})
