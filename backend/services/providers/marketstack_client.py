import requests
from core.upstream_error_handling import upstream_error_handling


class MarketStackClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.marketstack.com"
        self.api_key = api_key

    def search_tickers(self, query: str, ):
        url = f"{self.baseurl}/v2/tickerslist"
        params = {"search": query, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=5)

        upstream_error_handling(r)

        return r.json()

    def get_asset_eod(self, symbol: str):
        url = f"{self.baseurl}/v2/eod"
        params = {"symbols": symbol, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=5)

        upstream_error_handling(r)

        return r.json()

    # Backup (Marketstack v1)
    def search_tickers_backup(self, query: str, ):
        url = f"{self.baseurl}/v1/tickers"
        params = {"search": query, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=5)

        upstream_error_handling(r)

        return r.json()

    def get_asset_price_backup(self, symbol: str):
        url = f"{self.baseurl}/v1/eod"
        params = {"symbols": symbol, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=5)

        upstream_error_handling(r)

        return r.json()
