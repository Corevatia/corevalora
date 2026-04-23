from datetime import datetime, date
from sqlalchemy import Date, DateTime, Float, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id: Mapped[int] = mapped_column(primary_key=True)
    fetch_date: Mapped[date] = mapped_column(Date, index=True)
    base_currency: Mapped[str] = mapped_column(String(3))
    target_currency: Mapped[str] = mapped_column(String(3))
    rate: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("fetch_date", "base_currency", "target_currency"),
    )
