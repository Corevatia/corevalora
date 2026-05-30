import logging

from fastapi import APIRouter, HTTPException, Path, Depends, Request
from sqlalchemy.orm import Session

from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.stock import Stock, SearchResult
import services.stock_service as service
from typing import List
import requests

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/eod_price/{symbol}", response_model=Stock)
@limiter.limit("60/minute")
def stock_price(request: Request,symbol: str = Path(min_length=1, max_length=20, pattern=r"^[a-zA-Z0-9.]+$"),
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user),
                ):
    try:
        return service.get_price(symbol, db)
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 422:
            logger.error(f"Stock not found: {symbol}")
            raise HTTPException(status_code=404, detail="Stock not found")
        logger.error(f"Upstream error fetching stock price for {symbol}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout fetching stock price for {symbol}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error fetching stock price for {symbol}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")


@router.get("/search/{query}", response_model=List[SearchResult])
@limiter.limit("15/minute")
def stock_search(request: Request,query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\- ]+$"),
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    try:
        return service.get_stock_search(query, db)
    except requests.HTTPError as e:
        logger.error(f"Upstream error during stock search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout during stock search for {query}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error during stock search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")


@router.get("/search/backup/{query}", response_model=List[SearchResult])
@limiter.limit("15/minute")
def stock_search_backup(request: Request,query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\- ]+$"),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    try:
        return service.search_backup(query, db)
    except requests.HTTPError as e:
        logger.error(f"Upstream error during backup search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout during backup search for {query}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error during backup search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
