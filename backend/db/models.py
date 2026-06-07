from datetime import datetime, date
from sqlalchemy import Date, DateTime, Float, String, UniqueConstraint, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
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


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserSession(Base):
    __tablename__ = 'sessions'

    id: Mapped[str] = mapped_column(String(43), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Holding(Base):
    __tablename__ = 'holdings'
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    asset: Mapped[str] = mapped_column(String(255))
    symbol: Mapped[str] = mapped_column(String(10))
    amount: Mapped[float] = mapped_column(Float)
    avg_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    kind: Mapped[str] = mapped_column(String(10))

    __table_args__ = (
        UniqueConstraint("user_id", "key", "kind"),
    )


class AssetPriceCache(Base):
    __tablename__ = 'asset_price_cache'
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(10))
    key: Mapped[str] = mapped_column(String(50))
    symbol: Mapped[str] = mapped_column(String(10))
    asset_name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3))
    exchange: Mapped[str | None] = mapped_column(String(10), nullable=True)
    price_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    cached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("kind", "key"),)

class SearchCache(Base):
    __tablename__ = 'search_cache'
    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(10))
    query: Mapped[str] = mapped_column(String(50))
    results: Mapped[list] = mapped_column(JSONB)
    cached_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("kind", "query"),
    )


