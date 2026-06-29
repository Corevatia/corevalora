import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models.stock as stock
from services.currency.exchange_currency import get_exchange_currency
from services.cache.price_cache import read_price, is_fresh, upsert_price
from services.cache.search_cache import read_search, is_search_fresh, upsert_search
from services.providers.marketstack_client import MarketStackClient
import requests
from core.config import settings

from services.search_filter import filter_marketstack_search

logger = logging.getLogger(__name__)

client = MarketStackClient(api_key=settings.MARKETSTACK_API_KEY)


def get_stock_search(query: str, db: Session):
    if settings.MOCK_DATA:
        return [stock.SearchResult(name="StockXY", symbol="STXY", exchange="EXCHANGE", mic="EXCH")]

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
    upsert_search(db, kind="stock", query=query, results=[r.model_dump() for r in results])

    return results


def get_price(symbol: str, db: Session) -> stock.Stock:
    if settings.MOCK_DATA:
        return stock.Stock(symbol="STXY",
                           key="key",
                           price=123.45,
                           date="2026-02-23",
                           exchange="exch",
                           name="StockXY",
                           currency="CHF",
                           stale=False,
                           )

    cached = read_price(db, kind="stock", key=symbol)

    if cached and is_fresh(cached, "stock"):
        return _cache_to_stock(cached, stale=False)

    try:
        data = client.get_asset_eod(symbol)
        e = data["data"][0]

        try:
            upsert_price(
                db,
                kind="stock",
                key=e["symbol"],
                symbol=e["symbol"],
                asset_name=e["name"],
                price=float(e["close"]),
                currency=get_exchange_currency(e["exchange"]),
                exchange=e["exchange"],
                price_date=e["date"][:10],
            )
        except IntegrityError as e:
            if cached:
                logger.warning(f"Database Integrity error for stock {symbol} "
                                f"serving stale cache: {e}")
                return _cache_to_stock(cached, stale=True)
            raise

        return stock.Stock(
            key=e["symbol"],
            symbol=e["symbol"],
            price=float(e["close"]),
            date=e["date"][:10],
            exchange=e["exchange"],
            name=e["name"],
            currency=get_exchange_currency(e["exchange"]),
            stale=False,
        )
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None

        if status != 406 and status != 422:
            if status == 404:
                raise
            if cached:
                logger.warning(f"Upstream HTTP error for stock {symbol} "
                               f"serving stale cache: ´{e}")
                return _cache_to_stock(cached, stale=True)

        pricedata = client.get_asset_price_backup(symbol)
        p = pricedata["data"][0]

        infodata = client.search_tickers_backup(symbol)
        info = infodata["data"][0]

        try:
            upsert_price(
                db,
                kind="stock",
                key=p["symbol"],
                symbol=p["symbol"],
                asset_name=info["name"],
                price=float(p["close"]),
                currency=get_exchange_currency(p["exchange"]),
                exchange=p["exchange"],
                price_date=p["date"][:10],
            )
        except IntegrityError as e:
            if cached:
                logger.warning(f"Database Integrity error for stock {symbol} "
                                f"serving stale cache: {e}")
                return _cache_to_stock(cached, stale=True)
            raise

        return stock.Stock(
            key=p["symbol"],
            symbol=p["symbol"],
            price=float(p["close"]),
            date=p["date"][:10],
            exchange=p["exchange"],
            name=info["name"],
            currency=get_exchange_currency(p["exchange"]),
            stale=False,
        )
    except (requests.ConnectionError, requests.Timeout) as e:
        if cached:
            logger.warning(f"Upstream unreachable for stock {symbol} "
                           f"serving stale cache: {e}")
            return _cache_to_stock(cached, stale=True)
        raise


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
        return [stock.SearchResult(name="StockXY", symbol="STXY", exchange="EXCHANGE", mic="EXCH")]

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
    upsert_search(db, kind="bstock", query=query, results=[r.model_dump() for r in results])

    return results
