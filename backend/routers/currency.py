import logging

from fastapi import APIRouter, HTTPException, Path
import services.currency_service as service
import requests

from models.currency import RateResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates/{base_currency}", response_model=RateResponse)
def get_currency_rates(base_currency: str = Path(min_length=3, max_length=3, pattern=r"^[A-Z]+$")):
    try:
        return service.get_currency_rates(base_currency)
    except requests.HTTPError as e:
        logger.error(f"Upstream error fetching rates for {base_currency}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout fetching rates for {base_currency}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error fetching rates for {base_currency}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except KeyError:
        logger.error(f"Currency not found: {base_currency}")
        raise HTTPException(status_code=404, detail="Currency not found")
