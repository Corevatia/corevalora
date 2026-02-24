from fastapi import APIRouter, HTTPException
from models.stock import StockQuote, StockInfo
from services.stock_service import get_stock_price, get_stock_info
import requests

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/price/{symbol}", response_model=StockQuote)
def stock_price(symbol: str):
    try:
        return get_stock_price(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/info/{symbol}", response_model=StockInfo)
def stock_info(symbol: str, exchange: str):
    try:
        return get_stock_info(symbol, exchange)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
