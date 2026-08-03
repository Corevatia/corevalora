import logging
from urllib.parse import urlsplit

import requests

from core.config import settings
from core.errors import AssetNotFound, ProviderRejected, UpstreamUnavailable

logger = logging.getLogger(__name__)


def raise_for_upstream(r: requests.Response):
    if settings.UPSTREAM_DEBUG:
        logger.debug("Upstream status:%s, Upstream body:%s", r.status_code, r.text)
    if r.ok:
        return

    where = f"{urlsplit(r.url).path} -> {r.status_code}"
    logger.error("Upstream error: %s", where)
    if settings.UPSTREAM_DEBUG:
        logger.error("Upstream error body:%s", r.text)

    if r.status_code == 404:
        raise AssetNotFound(where)
    if r.status_code == 422:
        raise ProviderRejected(where)
    raise UpstreamUnavailable(where)
