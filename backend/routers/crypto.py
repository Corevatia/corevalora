from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.orm import Session

import services.crypto_service as service
from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.crypto import Crypto, SearchResult

router = APIRouter(prefix="/crypto", tags=["crypto"])


@router.get("/price/{asset_id}", response_model=Crypto)
@limiter.limit("60/minute")
def get_price(
    request: Request,
    asset_id: str = Path(min_length=1, max_length=50, pattern=r"^[a-z0-9\-]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_crypto_price(asset_id, db)


@router.get("/search/{query}", response_model=list[SearchResult])
@limiter.limit("15/minute")
def get_search_results(
    request: Request,
    query: str = Path(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9.\- ]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_crypto_search(query, db)
