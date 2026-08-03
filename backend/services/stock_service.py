import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models.stock as stock
from core.config import settings
from core.errors import AssetNotFound, ProviderRejected, UpstreamError
from services.cache.price_cache import is_fresh, read_price, upsert_price
from services.cache.search_cache import is_search_fresh, read_search, upsert_search
from services.exchanges.exchanges import get_exchange_currency
from services.exchanges.search_filter import filter_marketstack_search
from services.mocks.stock_mock import get_stock_mock, get_stock_search_results_mock
from services.providers.marketstack_client import MarketStackClient

logger = logging.getLogger(__name__)

client = MarketStackClient(api_key=settings.MARKETSTACK_API_KEY)


def get_stock_search(query: str, db: Session):
    if settings.MOCK_DATA:
        return get_stock_search_results_mock()

    cached = read_search(db, kind="stock", query=query)
    if cached and is_search_fresh(cached):
        return [stock.SearchResult(**r) for r in cached.results]

    data = client.search_tickers(query)
    filtered_data = filter_marketstack_search(data) or []
    results = [
        stock.SearchResult(
            key=e["ticker"],
            name=e["name"],
            symbol=e["ticker"],
            exchange=e["stock_exchange"]["name"],
            mic=e["stock_exchange"]["mic"],
        )
        for e in filtered_data
    ]
    upsert_search(
        db, kind="stock", query=query, results=[r.model_dump() for r in results]
    )

    return results


def get_price(symbol: str, db: Session) -> stock.Stock:
    if settings.MOCK_DATA:
        return get_stock_mock()

    cached = read_price(db, kind="stock", key=symbol)

    if cached and is_fresh(cached, "stock"):
        return _cache_to_stock(cached, stale=False)

    try:
        return _fetch_price(symbol, db)
    except AssetNotFound:
        raise
    except (UpstreamError, IntegrityError) as e:
        if cached:
            logger.warning(f"Could not refresh stock {symbol}, serving stale: {e}")
            return _cache_to_stock(cached, stale=True)
        raise


def _fetch_price(symbol: str, db: Session) -> stock.Stock:
    try:
        entry = client.get_asset_eod(symbol)["data"][0]
        name = entry["name"]
    except ProviderRejected as e:
        try:
            entry = client.get_asset_price_backup(symbol)["data"][0]
            name = client.search_tickers_backup(symbol)["data"][0]["name"]
        except ProviderRejected:
            raise AssetNotFound(f"{symbol} is not found") from e
    price = float(entry["close"])
    price_date = entry["date"][:10]
    currency = get_exchange_currency(entry["exchange"])

    upsert_price(
        db,
        kind="stock",
        key=entry["symbol"],
        symbol=entry["symbol"],
        asset_name=name,
        price=price,
        currency=currency,
        exchange=entry["exchange"],
        price_date=price_date,
    )
    return stock.Stock(
        key=entry["symbol"],
        symbol=entry["symbol"],
        name=name,
        price=price,
        date=price_date,
        exchange=entry["exchange"],
        currency=currency,
        stale=False,
    )


def _cache_to_stock(cached, stale: bool) -> stock.Stock:
    return stock.Stock(
        key=cached.key,
        symbol=cached.symbol,
        name=cached.asset_name,
        price=cached.price,
        date=cached.price_date.strftime("%Y-%m-%d"),
        exchange=cached.exchange,
        currency=cached.currency,
        stale=stale,
    )


def search_backup(query: str, db: Session):
    if settings.MOCK_DATA:
        return get_stock_search_results_mock()

    cached = read_search(db, kind="bstock", query=query)
    if cached and is_search_fresh(cached):
        return [stock.SearchResult(**r) for r in cached.results]

    data = client.search_tickers_backup(query)
    filtered_data = filter_marketstack_search(data) or []
    results = [
        stock.SearchResult(
            key=e["symbol"],
            name=e["name"],
            symbol=e["symbol"],
            exchange=e["stock_exchange"]["name"],
            mic=e["stock_exchange"]["mic"],
        )
        for e in filtered_data
    ]
    upsert_search(
        db, kind="bstock", query=query, results=[r.model_dump() for r in results]
    )

    return results
