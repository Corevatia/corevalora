import requests
from core.upstream_error_handling import upstream_error_handling

class FrankfurterClient:
    def __init__(self):
        self.base_url = "https://api.frankfurter.dev"
        self.session = requests.Session()

    def get_exchange_rate(self):
        url = f"{self.base_url}/v1/latest"
        r = self.session.get(url, timeout=5)

        upstream_error_handling(r)

        return r.json()