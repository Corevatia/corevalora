import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import InterfaceError, OperationalError
from starlette.responses import JSONResponse

from core.config import settings
from core.logging_config import setup_logging
from core.rate_limit import limiter
from db.database import SessionLocal
from routers.auth import router as auth_router
from routers.crypto import router as crypto_router
from routers.currency import router as currency_router
from routers.portfolio import router as portfolio_router
from routers.stock import router as stock_router
from services.auth.sessions import delete_expired_sessions
from services.cache.search_cache import delete_expired_search

setup_logging()
logger = logging.getLogger(__name__)

MAINTENANCE_CLEANUP_INTERVAL_SECONDS = 3600 * settings.MAINTENANCE_LOOP_HOURS

CLEANUP_TASKS = (
    ("expired sessions", delete_expired_sessions),
    ("expired searches", delete_expired_search),
)


def _run_cleanup(label, cleanup):
    try:
        with SessionLocal() as db:
            deleted = cleanup(db)
            if deleted:
                logger.info("Deleted %d %s", deleted, label)
    except Exception:
        logger.exception("Cleanup failed: %s", label)


async def _maintenance_loop():
    while True:
        for label, cleanup in CLEANUP_TASKS:
            _run_cleanup(label, cleanup)
        await asyncio.sleep(MAINTENANCE_CLEANUP_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_maintenance_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="CoreValora", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


async def _database_unavailable_handler(request: Request, exc: Exception):
    logger.error("Database unavailable on %s %s", request.method, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database unavailable"},
    )


app.add_exception_handler(OperationalError, _database_unavailable_handler)
app.add_exception_handler(InterfaceError, _database_unavailable_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crypto_router)
app.include_router(stock_router)
app.include_router(currency_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
