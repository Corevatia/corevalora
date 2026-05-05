from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
import logging

from core.auth_deps import get_current_user
from db.database import get_db
from db.models import User, Holding
from models.portfolio import HoldingOut, HoldingIn

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/Holdings", response_model=List[HoldingOut])
def list_holdings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.execute(
        select(Holding).where(Holding.user_id == current_user.id)
    ).scalars().all()
    return holdings


@router.post("/Holdings", response_model=HoldingOut, status_code=status.HTTP_201_CREATED)
def add_holding(
        data: HoldingIn,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    existing = db.execute(
        select(Holding).where(Holding.user_id == current_user.id,
                              Holding.symbol == data.symbol,
                              )
    ).scalar_one_or_none()

    if existing is None:
        holding = Holding(
            user_id=current_user.id,
            asset=data.asset,
            symbol=data.symbol,
            amount=data.amount,
            avg_price=data.buy_price
        )
        db.add(holding)
    else:
        new_amount = existing.amount + data.amount
        existing.avg_price = (existing.amount * existing.avg_price + data.amount * data.buy_price) / new_amount
        existing.amount = new_amount
        holding = existing

    db.commit()
    db.refresh(holding)
    return holding


@router.delete("/Holdings/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(
        symbol: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    holding = db.execute(
        select(Holding).where(
            Holding.user_id == current_user.id,
            Holding.symbol == symbol,
        )
    ).scalar_one_or_none()

    if holding is None:
        logger.error(f"Holding not found while deleting Symbol:{symbol}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found")

    db.delete(holding)
    db.commit()
