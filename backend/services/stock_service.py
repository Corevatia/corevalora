from pygments.lexers import data
import models.stock as stock
from services.exchange_currency import get_exchange_currency
from services.providers.marketstack_client import MarketStackClient
import dotenv
import os
import requests

from services.search_filter import filter_marketstack_search

dotenv.load_dotenv()

client = MarketStackClient(api_key=os.getenv("MARKETSTACK_API_KEY"))


def get_stock_search(query: str):
    if os.getenv("DEV_MODE") == "true":
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


def get_price(symbol: str) -> stock.Stock | None:
    if os.getenv("DEV_MODE") == "true":
        return stock.Stock(symbol="STXY",
                           price=123.45,
                           date="2026-02-23",
                           exchange="exch",
                           name="StockXY",
                           currency="CHF",
                           )

    try:
        data = client.get_asset_eod(symbol)
        rows = (data or {}).get("data") or []
        if rows:
            e = rows[0]
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
        try:
            pricedata = client.get_asset_price_backup(symbol)
            price_rows = (pricedata or {}).get("data") or []

            infodata = client.search_tickers_backup(symbol)
            info_rows = (infodata or {}).get("data") or []

            p = price_rows[0]
            return stock.Stock(
                symbol=p["symbol"],
                price=float(p["close"]),
                date=p["date"][:10] if isinstance(p.get("date"), str) else p["date"],
                exchange=p["exchange"],
                name=info_rows[0]["name"] if info_rows else symbol,
                currency=get_exchange_currency(p["exchange"]),
            )
        except requests.HTTPError as e:
            if e.response.status_code == 422:
                raise ValueError(404, f"cant find Symbol:{symbol}")
            raise


def search_backup(query: str):
    if os.getenv("DEV_MODE") == "true":
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

# clientAlphaVantage = AlphaVantageClient(api_key=os.getenv("ALPHAVANTAGE_API_KEY"))

# @router.get("/price/{symbol}")
# def get_price_alphavantage(symbol: str):
#     if os.getenv("DEV_MODE") == "true":
#         return {"price": 123.45, "symbol": "stockXY"}
#     try:
#         data = clientAlphaVantage.get_asset(symbol)
#         price = float(data["Global Quote"]["05. price"])
#         symbol = data["Global Quote"]["01. symbol"]
#         return {"price": price, "symbol": symbol}
#     except requests.HTTPError as e:
#         raise HTTPException(status_code=502, detail="Upstream API error")
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid asset id or response")
