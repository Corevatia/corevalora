from pydantic import BaseModel


class CryptoQuote(BaseModel):
    symbol: str
    price: float
    date: str
