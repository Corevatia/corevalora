from fastapi import Depends, HTTPException, APIRouter, status, Response, Cookie, Request
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.auth_deps import SESSION_COOKIE_NAME, get_current_user
from core.rate_limit import limiter
from core.config import settings
from db.database import get_db
from db.models import User
from models.auth import RegisterIn, UserOut, LoginIn
from services.auth.passwords import hash_password, verify_password
from services.auth.sessions import create_session, delete_session

SESSION_COOKIE_MAX_AGE = settings.SESSION_LIFETIME_DAYS * 24 * 60 * 60

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED, )
@limiter.limit("5/minute", key_func=get_remote_address)
def register(request: Request,data: RegisterIn, db: Session = Depends(get_db)):
    existing = db.execute(
        select(User).where(User.email == data.email)
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered", )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
@limiter.limit("5/minute", key_func=get_remote_address)
def login(request: Request,data: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.email == data.email)
    ).scalar_one_or_none()

    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    session = create_session(db, user.id)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session.id,
        max_age=SESSION_COOKIE_MAX_AGE,
        httponly=True,
        secure=False,  # In Prod: True
        samesite="lax",
        path="/",
    )
    return user


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
           db: Session = Depends(get_db)):
    if session_id is not None:
        delete_session(db, session_id)

    response.delete_cookie(key=SESSION_COOKIE_NAME,
                           path="/",
                           samesite="lax",
                           secure=False,  # same as Login-Cookie
                           )
