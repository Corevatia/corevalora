import logging

from fastapi import APIRouter, HTTPException
import services.crypto_service as service
import requests

from models.crypto import Crypto

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/price/{asset_id}", response_model=Crypto)
def get_price(asset_id: str):
    try:
        return service.get_crypto_price(asset_id)
    except ValueError as e:
        logger.warning(f"Crypto price not found for {asset_id}: {e}")
        raise HTTPException(status_code=404, detail="Crypto asset not found")
    except requests.HTTPError as e:
        logger.error(f"Upstream error fetching crypto price for {asset_id}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
