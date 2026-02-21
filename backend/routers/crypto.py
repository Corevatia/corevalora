from fastapi import APIRouter, HTTPException
from services.coincap_client import CoinCapClient
import requests

router = APIRouter(prefix="/crypto", tags=["crypto"])
client = CoinCapClient(api_key=None)  # später aus .env laden

@router.get("/price/{asset_id}")
def get_price(asset_id: str):
    try:
        data = client.get_asset(asset_id)
        price = float(data["data"]["priceUsd"])
        symbol = data["data"]["symbol"]
        return {"asset": asset_id, "priceUsd": price, "symbol": symbol}
    except requests.HTTPError as e:
        raise HTTPException(status_code=502, detail="Upstream API error")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid asset id or response")