from fastapi import APIRouter, HTTPException
import services.currency_service as service
import requests

from models.currency import RateResponse

router = APIRouter(prefix="/currency", tags=["currency"])

@router.get("/rates/{base_currency}", response_model=RateResponse)
def get_currency_rates(base_currency: str):
    try:
        return service.get_currency_rates(base_currency)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except requests.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))
