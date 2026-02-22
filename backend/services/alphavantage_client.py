import requests
from debug.upstream_debug import upstream_debug


class AlphaVantageClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://www.alphavantage.co/query"
        self.api_key = api_key

    def get_asset(self, symbol: str):
        r = self.session.get(self.baseurl,
                             params={"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self.api_key}, timeout=3)

        upstream_debug(r)

        return r.json()