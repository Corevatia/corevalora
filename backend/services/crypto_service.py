import dotenv
from services.providers.coincap_client import CoinCapClient
import os
import models.crypto as crypto
from datetime import datetime

dotenv.load_dotenv()
client = CoinCapClient(api_key=os.getenv("COINCAP_KEY"))

def get_crypto_price(asset_id: str):
    if os.getenv("DEV_MODE") == "true":
        return crypto.Crypto(
            symbol="XYC",
            name="XYCoin",
            price=123.45,
            currency="USD",
            date="2021-09-22",
        )

    data = client.get_asset(asset_id)
    price = float(data["data"]["priceUsd"])
    symbol = data["data"]["symbol"]
    name = data["data"]["name"]
    return crypto.Crypto(
        symbol=symbol,
        name=name,
        price=price,
        currency="USD",
        date=str(datetime.now().strftime("%Y-%m-%d %H:%M")),
    )