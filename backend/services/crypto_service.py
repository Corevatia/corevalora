import logging

import requests
from sqlalchemy.orm import Session

from services.price_cache import read_price, is_fresh, upsert_price
from services.providers.coincap_client import CoinCapClient
import models.crypto as crypto
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)

client = CoinCapClient(api_key=settings.COINCAP_API_KEY)


def get_crypto_price(asset_id: str, db: Session) -> crypto.Crypto:
    if settings.DEV_MODE:
        return crypto.Crypto(
            symbol="XYC",
            name="XYCoin",
            price=123.45,
            currency="USD",
            date="2021-09-22",
            stale=False,
        )

    cached = read_price(db, kind="crypto", key=asset_id)

    if cached and is_fresh(cached, "crypto"):
        return _cache_to_crypto(cached, stale=False)

    try:
        data = client.get_asset(asset_id)
        asset = data["data"]

        upsert_price(
            db,
            kind="crypto",
            key=asset_id,
            symbol=asset["symbol"],
            asset_name=asset["name"],
            price=float(asset["priceUsd"]),
            currency="USD",
            price_date=None,
        )

        return crypto.Crypto(
            symbol=asset["symbol"],
            name=asset["name"],
            price=float(asset["priceUsd"]),
            currency="USD",
            date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            stale=False,
        )
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            raise
        if cached:
            logger.warning(f"Upstream HTTP error for crypto {asset_id} "
                           f"serving stale cache: {e}")
            return _cache_to_crypto(cached, stale=True)
        raise
    except (requests.ConnectionError, requests.Timeout) as e:
        if cached:
            logger.warning(f"Upstream unreachable for crypto {asset_id} "
                           f"serving stale cache: {e}")
            return _cache_to_crypto(cached, stale=True)
        raise


def _cache_to_crypto(cached, stale: bool) -> crypto.Crypto:
    return crypto.Crypto(
        symbol=cached.symbol,
        name=cached.asset_name,
        price=cached.price,
        currency=cached.currency,
        date=cached.cached_at.strftime("%Y-%m-%d %H:%M"),
        stale=stale,
    )
