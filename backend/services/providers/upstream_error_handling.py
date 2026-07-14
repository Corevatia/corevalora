import requests
import logging
from core.config import settings

logger = logging.getLogger(__name__)


def upstream_error_handling(r: requests.Response):
    if settings.UPSTREAM_DEBUG:
        logger.debug("Upstream status:%s, Upstream body:%s", r.status_code, r.text)

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.error("HTTP ERROR:%s, Status:%s", e, r.status_code)
        if settings.UPSTREAM_DEBUG:
            logger.error("Upstream error body:%s", r.text)
        raise
