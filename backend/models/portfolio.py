from pydantic import BaseModel, ConfigDict, Field


class HoldingIn(BaseModel):
    asset: str
    key: str
    symbol: str
    amount: float = Field(gt=0)
    buy_price: float = Field(ge=0)
    kind: str


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
