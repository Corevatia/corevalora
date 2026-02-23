import requests
from debug.upstream_debug import upstream_debug


class MarketStackClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.marketstack.com/v1/eod"
        self.api_key = api_key

    def get_asset(self, symbol: str):
        r = self.session.get(self.baseurl,
                             params={"symbols": symbol, "access_key": self.api_key}, timeout=3)

        upstream_debug(r)

        return r.json()
