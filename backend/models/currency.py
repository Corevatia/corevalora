from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    symbol: str

class CurrencyRate(BaseModel):
    exchange_currency: str
    rate: float

class RateResponse(BaseModel):
    base_currency: str
    rates: list[CurrencyRate]