from fastapi import Cookie, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
from db.models import User
from services.auth.sessions import get_session

SESSION_COOKIE_NAME = "session_id"


def get_current_user(
    request: Request,
    session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    db: Session = Depends(get_db),
) -> User:
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    session = get_session(db, session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    user = db.execute(
        select(User).where(User.id == session.user_id)
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Stash for slowapi's key_func so the rate limit keys on the user, not the session
    request.state.user = user
    return user
