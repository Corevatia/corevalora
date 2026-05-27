import logging

from fastapi import APIRouter, HTTPException, Path, Depends, Request
from sqlalchemy.orm import Session

import services.crypto_service as service
import requests

from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.crypto import Crypto

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/price/{asset_id}", response_model=Crypto)
@limiter.limit("60/minute")
def get_price(request: Request,asset_id: str = Path(min_length=1, max_length=50, pattern=r"^[a-z0-9\-]+$"),
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user),
              ):
    try:
        return service.get_crypto_price(asset_id, db)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Crypto asset not found: {asset_id}")
            raise HTTPException(status_code=404, detail="Crypto asset not found")
        logger.error(f"Upstream error fetching crypto price for {asset_id}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
    except requests.Timeout:
        logger.error(f"Timeout fetching crypto price for {asset_id}")
        raise HTTPException(status_code=504, detail="External service timeout")
    except requests.ConnectionError as e:
        logger.error(f"Connection error fetching crypto price for {asset_id}: {e}")
        raise HTTPException(status_code=503, detail="External service unavailable")
