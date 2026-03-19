from fastapi import APIRouter, HTTPException
import services.crypto_service as service
import requests

from models.crypto import Crypto

router = APIRouter(prefix="/crypto", tags=["crypto"])

@router.get("/price/{asset_id}", response_model=Crypto)
def get_price(asset_id: str):
    try:
        return service.get_crypto_price(asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except requests.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))
