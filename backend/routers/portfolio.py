from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from core.auth_deps import get_current_user
from db.database import get_db
from db.models import User
from models.portfolio import HoldingIn, HoldingOut
from services import portfolio_service

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/holdings", response_model=List[HoldingOut])
def list_holdings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return portfolio_service.list_holdings(current_user, db)


@router.post("/holdings", response_model=HoldingOut, status_code=status.HTTP_201_CREATED)
def add_holding(
        data: HoldingIn,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return portfolio_service.add_holding(data, current_user, db)


@router.delete("/holdings/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(
        symbol: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    portfolio_service.delete_holding(symbol, current_user, db)
