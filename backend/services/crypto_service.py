import logging

import requests
from sqlalchemy.orm import Session

from services.cache.price_cache import read_price, is_fresh, upsert_price
from services.providers.coincap_client import CoinCapClient
import models.crypto as crypto
from datetime import datetime, timezone
from core.config import settings
from services.cache.search_cache import read_search, is_search_fresh, upsert_search

logger = logging.getLogger(__name__)

client = CoinCapClient(api_key=settings.COINCAP_API_KEY)


def get_crypto_price(asset_id: str, db: Session) -> crypto.Crypto:
    if settings.MOCK_DATA:
        return crypto.Crypto(
            key="key",
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
            key=asset_id,
            symbol=asset["symbol"],
            name=asset["name"],
            price=float(asset["priceUsd"]),
            currency="USD",
            date=datetime.now(timezone.utc).isoformat(),
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
        key=cached.key,
        symbol=cached.symbol,
        name=cached.asset_name,
        price=cached.price,
        currency=cached.currency,
        date=cached.cached_at.isoformat(),
        stale=stale,
    )


def get_crypto_search(query: str, db: Session):
    if settings.MOCK_DATA:
        return [crypto.SearchResult(symbol="KYC", name="KYCoin",rank=123)]

    cached = read_search(db, kind="crypto", query=query)
    if cached and is_search_fresh(cached):
        return  [crypto.SearchResult(**r) for r in cached.results]

    data = client.search_assets(query)
    results = [
        crypto.SearchResult(
            key=e["id"],
            symbol=e["symbol"],
            name=e["name"],
            rank=int(e["rank"]),
        )
        for e in data["data"]
    ]
    upsert_search(db, kind="crypto", query=query, results=[r.model_dump() for r in results])

    return results

