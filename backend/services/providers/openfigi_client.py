import requests

from core.errors import UpstreamTimeout, UpstreamUnavailable
from services.providers.upstream_error_handling import raise_for_upstream

JOBS_PER_REQUEST_WITH_KEY = 100
JOBS_PER_REQUEST_WITHOUT_KEY = 10


class OpenFigiClient:
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.base_url = "https://api.openfigi.com"
        self.api_key = api_key
        if api_key:
            self.session.headers.update({"X-OPENFIGI-APIKEY": api_key})

    def _post(self, url: str, payload: list) -> list:
        try:
            r = self.session.post(url, json=payload, timeout=5)
        except requests.Timeout as e:
            raise UpstreamTimeout(f"OpenFIGI timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"OpenFIGI unreachable: {url}") from e

        raise_for_upstream(r)
        return r.json()

    def map_tickers(self, jobs: list[dict]) -> list[dict]:
        size = (
            JOBS_PER_REQUEST_WITH_KEY if self.api_key else JOBS_PER_REQUEST_WITHOUT_KEY
        )
        results = []
        for i in range(0, len(jobs), size):
            results.extend(
                self._post(f"{self.base_url}/v3/mapping", jobs[i : i + size])
            )
        return results
