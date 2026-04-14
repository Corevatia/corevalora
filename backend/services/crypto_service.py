from fastapi import HTTPException
import logging
from services.providers.coincap_client import CoinCapClient
import models.crypto as crypto
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)

client = CoinCapClient(api_key=settings.COINCAP_API_KEY)


def get_crypto_price(asset_id: str):
    if settings.DEV_MODE:
        return crypto.Crypto(
            symbol="XYC",
            name="XYCoin",
            price=123.45,
            currency="USD",
            date="2021-09-22",
        )

    data = client.get_asset(asset_id)
    try:
        price = float(data["data"]["priceUsd"])
        symbol = data["data"]["symbol"]
        name = data["data"]["name"]
    except KeyError:
        logger.error(f"{asset_id} has no/invalid data")
        raise HTTPException(status_code=400, detail="Invalid crypto price data")

    return crypto.Crypto(
        symbol=symbol,
        name=name,
        price=price,
        currency="USD",
        date=str(datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
