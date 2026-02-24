import requests
from debug.upstream_debug import upstream_debug


class MarketStackClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.marketstack.com"
        self.api_key = api_key

    def get_asset_price(self, symbol: str):
        url = f"{self.baseurl}/v1/eod"
        params = {"symbols": symbol, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=3)

        upstream_debug(r)

        return r.json()

    def get_asset_info(self, symbol: str, exchange: str):
        url = f"{self.baseurl}/v1/tickers"
        params = {"search": symbol, "exchange": exchange, "access_key": self.api_key}
        r = self.session.get(url, params=params, timeout=3)

        upstream_debug(r)

        return r.json()
