from pydantic import BaseModel


class StockInfo(BaseModel):
    name: str
    currency: str


class StockQuote(BaseModel):
    symbol: str
    price: float
    date: str
    exchange: str
