import secrets
from db.models import UserSession
from sqlalchemy.orm import Session
from sqlalchemy import delete
from datetime import datetime, timedelta, timezone
from core.config import settings

SESSION_LIFETIME = timedelta(days=settings.SESSION_LIFETIME_DAYS)


def create_session(db: Session, user_id: int) -> UserSession:
    session_id = secrets.token_urlsafe(32)
    expire_at = datetime.now(timezone.utc) + SESSION_LIFETIME

    session = UserSession(
        id=session_id,
        user_id=user_id,
        expires_at=expire_at,
    )
    db.add(session)
    db.commit()
    return session


def get_session(db: Session, session_id: str) -> UserSession | None:
    session = db.get(UserSession, session_id)
    if session is None:
        return None

    if session.expires_at < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        return None

    return session


def delete_session(db, session_id) -> None:
    session = db.get(UserSession, session_id)
    if session is not None:
        db.delete(session)
        db.commit()

def delete_expired_sessions(db: Session) -> int:
    result = db.execute(
        delete(UserSession).where(UserSession.expires_at < datetime.now(timezone.utc))
        )

    db.commit()
    return result.rowcount

