from datetime import datetime, timedelta, timezone
import secrets

from core.auth_deps import SESSION_COOKIE_NAME
from db.models import UserSession


def test_me_returns_logged_in_user(auth_client, user):
    resp = auth_client.get('/auth/me')

    assert resp.status_code == 200
    assert resp.json()["email"] == user.email

def test_me_without_session_is_unauthorized(client):
    resp = client.get('/auth/me')

    assert resp.status_code == 401

def test_me_unknown_session_is_unauthorized(client):
    client.cookies.set(SESSION_COOKIE_NAME, "unknown_session")
    resp = client.get('/auth/me')

    assert resp.status_code == 401

def test_me_with_expired_session(client, db, user):
    expired = UserSession(id=secrets.token_urlsafe(32), user_id=user.id, expires_at=datetime.now(timezone.utc) - timedelta(days=1))
    db.add(expired)
    db.flush()
    client.cookies.set(SESSION_COOKIE_NAME, expired.id)

    resp = client.get('/auth/me')

    assert resp.status_code == 401
    assert db.get(UserSession, expired.id) is None