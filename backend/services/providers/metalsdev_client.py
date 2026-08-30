import logging

import requests

from core.errors import (
    AssetNotFound,
    ProviderRejected,
    UpstreamTimeout,
    UpstreamUnavailable,
)
from services.providers.upstream_error_handling import raise_for_upstream

logger = logging.getLogger(__name__)

LATEST_PATH = "/v1/latest"


def raise_for_metals_status(data: dict, where: str) -> None:
    if data.get("status") == "success" and "metals" in data:
        return

    e = data.get("error_code")
    message = data.get("error_message")
    logger.error("Upstream error: %s -> %s code:%s", where, message, e)
    if e == 1203:
        raise ProviderRejected(f"{where}: {message}")
    raise UpstreamUnavailable(f"{where}: {message}")


class MetalsDevClient:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.baseurl = "https://api.metals.dev"
        self.api_key = api_key

    def _get(self, url: str, params: dict) -> dict:
        try:
            r = self.session.get(
                url, params={**params, "api_key": self.api_key}, timeout=5
            )
        except requests.Timeout as e:
            raise UpstreamTimeout(f"Metals.Dev timeout: {url}") from e
        except requests.ConnectionError as e:
            raise UpstreamUnavailable(f"Metals.Dev unreachable: {url}") from e

        raise_for_upstream(r)

        return r.json()

    def get_latest_metals(self) -> dict:
        try:
            data = self._get(
                f"{self.baseurl}{LATEST_PATH}", {"unit": "g", "currency": "USD"}
            )
        except AssetNotFound as e:
            raise UpstreamUnavailable(f"Metals.Dev endpoint missing: {e}") from e

        raise_for_metals_status(data, where=LATEST_PATH)

        return data
