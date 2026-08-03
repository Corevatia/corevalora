import requests

from core.errors import UpstreamTimeout, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream


class FrankfurterClient:
    def __init__(self):
        self.base_url = "https://api.frankfurter.dev"
        self.session = requests.Session()

    def get_exchange_rate(self):
        url = f"{self.base_url}/v1/latest"
        try:
            r = self.session.get(url, timeout=5)
        except requests.Timeout as e:
            raise UpstreamTimeout(f"Frankfurter timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"Frankfurter unreachable: {url}") from e

        raise_for_upstream(r)

        return r.json()
