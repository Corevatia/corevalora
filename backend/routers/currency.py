import logging

from fastapi import APIRouter, HTTPException
import services.currency_service as service
import requests

from models.currency import RateResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates/{base_currency}", response_model=RateResponse)
def get_currency_rates(base_currency: str):
    try:
        return service.get_currency_rates(base_currency)
    except ValueError as e:
        logger.warning(f"Currency rates not found for {base_currency}: {e}")
        raise HTTPException(status_code=404, detail="Currency not found")
    except requests.HTTPError as e:
        logger.error(f"Upstream error fetching rates for {base_currency}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
