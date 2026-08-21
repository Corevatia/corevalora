from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Temporary so frontend keeps working
class HoldingIn(BaseModel):
    asset: str
    key: str
    symbol: str
    amount: float = Field(gt=0)
    buy_price: float = Field(ge=0)
    kind: str


class TransactionIn(BaseModel):
    asset: str
    key: str
    symbol: str
    kind: str
    side: Literal["buy", "sell"]
    amount: float = Field(gt=0)
    price: float = Field(ge=0)
    traded_on: date

    @field_validator("traded_on")
    @classmethod
    def reject_future_trade_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Trade date cannot be in the future")
        return value


class TransactionOut(BaseModel):
    id: int
    side: str
    amount: float
    price: float
    traded_on: date

    model_config = ConfigDict(from_attributes=True)


class HoldingOut(BaseModel):
    id: int
    asset: str
    key: str
    symbol: str
    kind: str
    amount: float
    avg_price: float
    price: float | None = None
    currency: str | None = None
    exchange: str | None = None
    price_date: str | None = None
    stale: bool

    model_config = ConfigDict(from_attributes=True)
