from fastapi import APIRouter, HTTPException
from services.alphavantage_client import AlphaVantageClient
import requests
import dotenv
import os

dotenv.load_dotenv()

router = APIRouter(prefix="/stock", tags=["stock"])
client = AlphaVantageClient(api_key=os.getenv("ALPHAVANTAGE_API_KEY"))


@router.get("/price/{symbol}")
def get_price(symbol: str):
    if os.getenv("DEV_MODE") == "true":
        return {"price": 123.45, "symbol": "Crackstock"}
    try:
        data = client.get_asset(symbol)
        price = float(data["Global Quote"]["05. price"])
        symbol = data["Global Quote"]["01. symbol"]
        return {"price": price, "symbol": symbol}
    except requests.HTTPError as e:
        raise HTTPException(status_code=502, detail="Upstream API error")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid asset id or response")
