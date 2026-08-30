from pydantic import BaseModel


class Metal(BaseModel):
    key: str
    symbol: str
    name: str
    price: float
    currency: str
    date: str
    stale: bool


class SupportedMetal(BaseModel):
    key: str
    name: str
    symbol: str
