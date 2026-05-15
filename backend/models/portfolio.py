from pydantic import BaseModel, Field, ConfigDict


class HoldingIn(BaseModel):
    asset: str
    symbol: str
    amount: float = Field(gt=0)
    buy_price: float = Field(ge=0)
    kind: str


class HoldingOut(BaseModel):
    id: int
    asset: str
    symbol: str
    kind: str
    amount: float
    avg_price: float
    price: float
    currency: str
    exchange: str | None = None
    price_date: str
    stale: bool

    model_config = ConfigDict(from_attributes=True)
