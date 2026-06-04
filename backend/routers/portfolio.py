from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status

from core.rate_limit import limiter
from core.auth_deps import get_current_user
from db.database import get_db
from db.models import User
from models.portfolio import HoldingIn, HoldingOut
from services import portfolio_service

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/holdings", response_model=List[HoldingOut])
@limiter.limit("120/minute")
def list_holdings(request: Request,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return portfolio_service.list_holdings(current_user, db)


@router.post("/holdings", response_model=HoldingOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def add_holding(
        request: Request,
        data: HoldingIn,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return portfolio_service.add_holding(data, current_user, db)


@router.delete("/holdings/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("20/minute")
def delete_holding(
        request: Request,
        holding_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    portfolio_service.delete_holding(holding_id, current_user, db)
