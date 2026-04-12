import requests
import logging
from core.config import settings

logger = logging.getLogger(__name__)


def upstream_error_handling(r: requests.Response):
    if settings.UPSTREAM_DEBUG:
        logger.debug(f"Upstream status:{r.status_code},Upstream body:{r.text[:100]}")

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.error(f"HTTP ERROR:{e},Status:{r.status_code},Body:{r.text[:100]}")
        raise
