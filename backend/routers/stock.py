from fastapi import APIRouter, HTTPException
from models.stock import Stock, SearchResult
import services.stock_service as service
from typing import List
import requests

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/eod_price/{symbol}", response_model=Stock)
def stock_price(symbol: str):
    try:
        return service.get_price(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except requests.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/search/{query}", response_model=List[SearchResult])
def stock_search(query: str):
    try:
        return service.get_stock_search(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except requests.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/search/backup/{query}", response_model=List[SearchResult])
def stock_search_backup(query: str, ):
    try:
        return service.search_backup(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except requests.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))
