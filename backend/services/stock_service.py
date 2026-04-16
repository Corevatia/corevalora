import models.stock as stock
from services.currency.exchange_currency import get_exchange_currency
from services.providers.marketstack_client import MarketStackClient
import requests
from core.config import settings

from services.search_filter import filter_marketstack_search

client = MarketStackClient(api_key=settings.MARKETSTACK_API_KEY)


def get_stock_search(query: str):
    if settings.DEV_MODE:
        return [stock.SearchResult(name="StockXY", symbol="STXY", exchange="EXCHANGE", mic="EXCH")]

    data = client.search_tickers(query)
    filtered_data = filter_marketstack_search(data) or []
    results = [
        stock.SearchResult(
            name=e["name"],
            symbol=e["ticker"],
            exchange=e["stock_exchange"]["name"],
            mic=e["stock_exchange"]["mic"],
        )
        for e in filtered_data
    ]
    return results


def get_price(symbol: str) -> stock.Stock:
    if settings.DEV_MODE:
        return stock.Stock(symbol="STXY",
                           price=123.45,
                           date="2026-02-23",
                           exchange="exch",
                           name="StockXY",
                           currency="CHF",
                           )

    try:
        data = client.get_asset_eod(symbol)
        e = data["data"][0]
        return stock.Stock(
            symbol=e["symbol"],
            price=float(e["close"]),
            date=e["date"][:10],
            exchange=e["exchange"],
            name=e["name"],
            currency=e["price_currency"],
        )
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None

        if status != 406:
            raise

        pricedata = client.get_asset_price_backup(symbol)
        p = pricedata["data"][0]

        infodata = client.search_tickers_backup(symbol)
        info = infodata["data"][0]

        return stock.Stock(
            symbol=p["symbol"],
            price=float(p["close"]),
            date=p["date"][:10],
            exchange=p["exchange"],
            name=info["name"],
            currency=get_exchange_currency(p["exchange"]),
        )


def search_backup(query: str):
    if settings.DEV_MODE:
        return [stock.SearchResult(name="StockXY", symbol="STXY", exchange="EXCHANGE", mic="EXCH")]

    data = client.search_tickers_backup(query)
    filtered_data = filter_marketstack_search(data) or []
    results = [
        stock.SearchResult(
            name=e["name"],
            symbol=e["symbol"],
            exchange=e["stock_exchange"]["name"],
            mic=e["stock_exchange"]["mic"],
        )
        for e in filtered_data
    ]
    return results
