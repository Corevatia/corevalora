from pydantic import BaseModel


class Crypto(BaseModel):
    symbol: str
    name: str
    price: float
    currency: str
    date: str
    stale: bool = False
