import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from core.auth_deps import SESSION_COOKIE_NAME
from db import models
from db.database import get_db
from main import app
from services.auth.sessions import create_session

TEST_DB_URL = os.environ.get(
    "TEST_DB_URL",
    "postgresql+psycopg://corevalora:test@localhost:5432/corevalora_test",
)

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine)

BACKEND_DIR = Path(__file__).resolve().parents[1]
ALEMBIC_INI = BACKEND_DIR / "alembic.ini"

@pytest.fixture(scope="session", autouse=True)
def _migrate_test_db():
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))

        os.environ["ALEMBIC_DB_URL"] = TEST_DB_URL

        cfg = Config(str(ALEMBIC_INI))
        command.upgrade(cfg, "head")

        yield


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(
        bind=connection, join_transaction_mode="create_savepoint"
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def user(db):
    u = models.User(email="test@example.com", hashed_password="x" * 60)
    db.add(u)
    db.flush()
    return u

@pytest.fixture
def holding(db, user):
    h = models.Holding(
        key="bitcoin",
        user_id=user.id,
        asset="Bitcoin",
        symbol="BTC",
        amount=2.5,
        avg_price=40000,
        kind="crypto",
    )
    db.add(h)
    db.flush()
    return h

@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def auth_client(client, db, user):
    session = create_session(db, user.id)
    client.cookies.set(SESSION_COOKIE_NAME, session.id)
    return client