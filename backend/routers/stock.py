from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.orm import Session

import services.stock_service as service
from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.stock import SearchResult, Stock

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/eod_price/{symbol}", response_model=Stock)
@limiter.limit("60/minute")
def stock_price(
    request: Request,
    symbol: str = Path(min_length=1, max_length=20, pattern=r"^[a-zA-Z0-9.-]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_price(symbol, db)


@router.get("/search/{query}", response_model=list[SearchResult])
@limiter.limit("15/minute")
def stock_search(
    request: Request,
    query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\-& ]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_stock_search(query, db)


@router.get("/search/backup/{query}", response_model=list[SearchResult])
@limiter.limit("15/minute")
def stock_search_backup(
    request: Request,
    query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\-& ]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.search_backup(query, db)
