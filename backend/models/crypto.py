from pydantic import BaseModel


class Crypto(BaseModel):
    key: str
    symbol: str
    name: str
    price: float
    currency: str
    date: str
    stale: bool = False


class SearchResult(BaseModel):
    key: str
    name: str
    symbol: str
    rank: int
