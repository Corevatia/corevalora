import models.stock as stock
from models.stock import StockInfo
from services.exchange_currency import get_exchange_currency
from services.providers.marketstack_client import MarketStackClient
import dotenv
import os

dotenv.load_dotenv()

client = MarketStackClient(api_key=os.getenv("MARKETSTACK_API_KEY"))


def get_stock_price(symbol: str) -> stock.StockQuote:
    if os.getenv("DEV_MODE") == "true":
        return stock.StockQuote(symbol="STXY",
                                price=123.45,
                                date="2026-02-23,",
                                exchange="exch",
                                )

    data = client.get_asset_price(symbol)

    return stock.StockQuote(symbol=data["data"][0]["symbol"],
                            price=float(data["data"][0]["close"]),
                            date=data["data"][0]["date"],
                            exchange=data["data"][0]["exchange"],
                            )


def get_stock_info(symbol: str, exchange: str) -> stock.StockInfo:
    if os.getenv("DEV_MODE") == "true":
        return StockInfo(name="STXY", currency="CHF")

    data = client.get_asset_info(symbol, exchange)
    currency = get_exchange_currency(data["data"][0]["stock_exchange"]["mic"])
    return stock.StockInfo(name=data["data"][0]["name"], currency=currency)

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
