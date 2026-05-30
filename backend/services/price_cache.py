from datetime import datetime, date, timezone

from core.config import settings
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from db.models import AssetPriceCache

CACHE_TTL_SECONDS = {"crypto": settings.CRYPTO_CACHE_TTL_SECONDS, "stock": 1440 * settings.STOCK_CACHE_TTL_HOURS}


def read_price(db, kind, key) -> AssetPriceCache | None:
    return db.execute(
        select(AssetPriceCache).where(
            AssetPriceCache.kind == kind,
            AssetPriceCache.key == key
        )
    ).scalar_one_or_none()


def is_fresh(cached, kind) -> bool:
    age = (datetime.now(timezone.utc) - cached.cached_at).total_seconds()
    return age < CACHE_TTL_SECONDS[kind]


def upsert_price(
        db: Session,
        *,
        kind: str,
        key: str,
        symbol: str,
        asset_name: str,
        price: float,
        currency: str,
        exchange: str | None = None,
        price_date: date | None = None
) -> None:
    stmt = insert(AssetPriceCache).values(
        kind=kind,
        key=key,
        symbol=symbol,
        asset_name=asset_name,
        price=price,
        currency=currency,
        exchange=exchange,
        price_date=price_date,
        cached_at=datetime.now(timezone.utc),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["kind", "key"],
        set_={
            "asset_name": stmt.excluded.asset_name,
            "symbol": stmt.excluded.symbol,
            "price": stmt.excluded.price,
            "currency": stmt.excluded.currency,
            "exchange": stmt.excluded.exchange,
            "price_date": stmt.excluded.price_date,
            "cached_at": stmt.excluded.cached_at,
        }
    )
    db.execute(stmt)
    db.commit()
