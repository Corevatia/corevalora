import requests
from core.upstream_error_handling import upstream_error_handling


class CoinCapClient:
    def __init__(self, api_key):
        self.base_url = "https://rest.coincap.io"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get_asset(self, asset_id: str) -> dict:
        url = f"{self.base_url}/v3/assets/{asset_id}"
        r = self.session.get(url, timeout=2)

        upstream_error_handling(r)

        return r.json()
