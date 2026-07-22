import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.orm import Session
from starlette import status

from db.models import Holding, User
from models.portfolio import HoldingIn, HoldingOut
from services import crypto_service, stock_service

logger = logging.getLogger(__name__)


def compute_avg_price(
    old_amount: float, old_avg: float, add_amount: float, add_price: float
) -> tuple[float, float]:
    new_amount = old_amount + add_amount
    new_avg = (old_amount * old_avg + add_amount * add_price) / new_amount
    return new_amount, new_avg


def list_holdings(user: User, db: Session) -> list[HoldingOut]:
    holdings = (
        db.execute(select(Holding).where(Holding.user_id == user.id)).scalars().all()
    )
    return [_safe_enrich_holding(h, db) for h in holdings]


def _safe_enrich_holding(holding: Holding, db: Session) -> HoldingOut:
    try:
        return _enrich_holding(holding, db)
    except (OperationalError, InterfaceError):
        raise
    except Exception:
        logger.exception(
            "Failed to price holding id=%s key=%s; returning degraded entry",
            holding.id,
            holding.key,
        )
        return HoldingOut(
            id=holding.id,
            asset=holding.asset,
            key=holding.key,
            symbol=holding.symbol,
            kind=holding.kind,
            amount=holding.amount,
            avg_price=holding.avg_price,
            price=None,
            currency=None,
            exchange=None,
            price_date=None,
            stale=True,
        )


def add_holding(data: HoldingIn, user: User, db: Session) -> HoldingOut:
    existing = db.execute(
        select(Holding).where(
            Holding.user_id == user.id,
            Holding.key == data.key,
            Holding.kind == data.kind,
        )
    ).scalar_one_or_none()

    if existing is None:
        holding = Holding(
            key=data.key,
            user_id=user.id,
            asset=data.asset,
            symbol=data.symbol,
            kind=data.kind,
            amount=data.amount,
            avg_price=data.buy_price,
        )
        db.add(holding)
    else:
        existing.amount, existing.avg_price = compute_avg_price(
            existing.amount, existing.avg_price, data.amount, data.buy_price
        )
        holding = existing

    db.commit()
    db.refresh(holding)
    return _enrich_holding(holding, db)


def delete_holding(holding_id: int, user: User, db: Session) -> None:
    holding = db.execute(
        select(Holding).where(
            Holding.id == holding_id,
            Holding.user_id == user.id,
        )
    ).scalar_one_or_none()

    if holding is None:
        logger.error(f"Holding not found while deleting id:{holding_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found"
        )

    db.delete(holding)
    db.commit()


def _enrich_holding(holding: Holding, db: Session) -> HoldingOut:
    if holding.kind == "crypto":
        priced = crypto_service.get_crypto_price(holding.key, db)
        exchange = None
    else:
        priced = stock_service.get_price(holding.key, db)
        exchange = priced.exchange

    return HoldingOut(
        id=holding.id,
        asset=holding.asset,
        key=holding.key,
        symbol=holding.symbol,
        kind=holding.kind,
        amount=holding.amount,
        avg_price=holding.avg_price,
        price=priced.price,
        currency=priced.currency,
        exchange=exchange,
        price_date=priced.date,
        stale=priced.stale,
    )
