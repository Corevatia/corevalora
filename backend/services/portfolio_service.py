import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from db.models import Holding, User
from models.portfolio import HoldingIn, HoldingOut
from services import crypto_service, stock_service

logger = logging.getLogger(__name__)


def list_holdings(user: User, db: Session) -> list[HoldingOut]:
    holdings = db.execute(
        select(Holding).where(Holding.user_id == user.id)
    ).scalars().all()
    return [_enrich_holding(h, db) for h in holdings]


def add_holding(data: HoldingIn, user: User, db: Session) -> HoldingOut:
    existing = db.execute(
        select(Holding).where(
            Holding.user_id == user.id,
            Holding.symbol == data.symbol,
            Holding.kind == data.kind,
        )
    ).scalar_one_or_none()

    if existing is None:
        holding = Holding(
            user_id=user.id,
            asset=data.asset,
            symbol=data.symbol,
            kind=data.kind,
            amount=data.amount,
            avg_price=data.buy_price,
        )
        db.add(holding)
    else:
        new_amount = existing.amount + data.amount
        existing.avg_price = (
                                     existing.amount * existing.avg_price + data.amount * data.buy_price
                             ) / new_amount
        existing.amount = new_amount
        holding = existing

    db.commit()
    db.refresh(holding)
    return _enrich_holding(holding, db)


def delete_holding(symbol: str, user: User, db: Session) -> None:
    holding = db.execute(
        select(Holding).where(
            Holding.user_id == user.id,
            Holding.symbol == symbol,
        )
    ).scalar_one_or_none()

    if holding is None:
        logger.error(f"Holding not found while deleting Symbol:{symbol}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found")

    db.delete(holding)
    db.commit()


def _enrich_holding(holding: Holding, db: Session) -> HoldingOut:
    if holding.kind == "crypto":
        priced = crypto_service.get_crypto_price(holding.asset.lower(), db)
        exchange = None
    else:
        priced = stock_service.get_price(holding.symbol, db)
        exchange = priced.exchange

    return HoldingOut(
        id=holding.id,
        asset=holding.asset,
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
