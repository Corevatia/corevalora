from pydantic import BaseModel


class SearchResult(BaseModel):
    name: str
    symbol: str
    exchange: str
    mic: str


class Stock(BaseModel):
    symbol: str
    price: float
    date: str
    exchange: str
    name: str
    currency: str
    stale: bool = False
