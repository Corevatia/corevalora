from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy.orm import Session

import services.currency_service as service
from core.auth_deps import get_current_user
from core.rate_limit import limiter
from db.database import get_db
from db.models import User
from models.currency import RateResponse

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates/{base_currency}", response_model=RateResponse)
@limiter.limit("120/minute")
def get_currency_rates(
    request: Request,
    base_currency: Annotated[
        str, Path(min_length=3, max_length=3, pattern=r"^[A-Z]+$")
    ],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_currency_rates(base_currency, db)
