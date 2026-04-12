import logging

from fastapi import APIRouter, HTTPException
from models.stock import Stock, SearchResult
import services.stock_service as service
from typing import List
import requests

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/eod_price/{symbol}", response_model=Stock)
def stock_price(symbol: str):
    try:
        return service.get_price(symbol)
    except ValueError as e:
        logger.warning(f"Stock price not found for {symbol}: {e}")
        raise HTTPException(status_code=404, detail="Stock not found")
    except requests.HTTPError as e:
        logger.error(f"Upstream error fetching stock price for {symbol}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")


@router.get("/search/{query}", response_model=List[SearchResult])
def stock_search(query: str):
    try:
        return service.get_stock_search(query)
    except ValueError as e:
        logger.warning(f"Stock search failed for {query}: {e}")
        raise HTTPException(status_code=404, detail="No results found")
    except requests.HTTPError as e:
        logger.error(f"Upstream error during stock search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")


@router.get("/search/backup/{query}", response_model=List[SearchResult])
def stock_search_backup(query: str):
    try:
        return service.search_backup(query)
    except ValueError as e:
        logger.warning(f"Stock backup search failed for {query}: {e}")
        raise HTTPException(status_code=404, detail="No results found")
    except requests.HTTPError as e:
        logger.error(f"Upstream error during backup search for {query}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
