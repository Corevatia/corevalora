from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.orm import Session

import services.metal_service as service
from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.metal import Metal, SupportedMetal

router = APIRouter(prefix="/metal", tags=["metal"])


@router.get("/price/{key}", response_model=Metal)
@limiter.limit("60/minute")
def get_price(
    request: Request,
    key: str = Path(min_length=1, max_length=10, pattern=r"^[a-z]+$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_price(key, db)


@router.get("/supported", response_model=list[SupportedMetal])
@limiter.limit("30/minute")
def get_supported_metals(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_supported_metals()
