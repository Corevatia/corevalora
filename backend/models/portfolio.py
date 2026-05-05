from pydantic import BaseModel, Field, ConfigDict


class HoldingIn(BaseModel):
    asset: str
    symbol: str
    amount: float = Field(gt=0)
    buy_price: float = Field(ge=0)


class HoldingOut(BaseModel):
    id: int
    asset: str
    symbol: str
    amount: float
    avg_price: float

    model_config = ConfigDict(from_attributes=True)
