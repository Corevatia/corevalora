import logging

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.stock import Stock, SearchResult
import services.stock_service as service
from typing import List
import requests

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/eod_price/{symbol}", response_model=Stock)
def stock_price(symbol: str = Path(min_length=1, max_length=20, pattern=r"^[a-zA-Z0-9.]+$"),
                db: Session = Depends(get_db),
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
def stock_search(query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\- ]+$")):
    try:
        return service.get_stock_search(query)
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
def stock_search_backup(query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\- ]+$")):
    try:
        return service.search_backup(query)
    except requests.HTTPError as e:
        logger.error(f"Upstream error during backup search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout during backup search for {query}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error during backup search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
