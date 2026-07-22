import logging
from datetime import UTC, datetime

import requests
from sqlalchemy.orm import Session

import models.crypto as crypto
from core.config import settings
from services.cache.price_cache import is_fresh, read_price, upsert_price
from services.cache.search_cache import is_search_fresh, read_search, upsert_search
from services.mocks.crypto_mock import get_crypto_mock, get_crypto_search_results_mock
from services.providers.coincap_client import CoinCapClient

logger = logging.getLogger(__name__)

client = CoinCapClient(api_key=settings.COINCAP_API_KEY)


def get_crypto_price(asset_id: str, db: Session) -> crypto.Crypto:
    if settings.MOCK_DATA:
        return get_crypto_mock()

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
            date=datetime.now(UTC).isoformat(),
            stale=False,
        )
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            raise
        if cached:
            logger.warning(
                f"Upstream HTTP error for crypto {asset_id} serving stale cache: {e}"
            )
            return _cache_to_crypto(cached, stale=True)
        raise
    except (requests.ConnectionError, requests.Timeout) as e:
        if cached:
            logger.warning(
                f"Upstream unreachable for crypto {asset_id} serving stale cache: {e}"
            )
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
        return get_crypto_search_results_mock()

    cached = read_search(db, kind="crypto", query=query)
    if cached and is_search_fresh(cached):
        return [crypto.SearchResult(**r) for r in cached.results]

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
    upsert_search(
        db, kind="crypto", query=query, results=[r.model_dump() for r in results]
    )

    return results
