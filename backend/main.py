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
from core.errors import (
    AssetNotFound,
    HoldingNotFound,
    InsufficientHoldingAmount,
    TransactionNotFound,
    UnknownCurrency,
    UpstreamError,
    UpstreamTimeout,
)
from core.logging_config import setup_logging
from core.rate_limit import limiter
from db.database import SessionLocal
from routers.auth import router as auth_router
from routers.crypto import router as crypto_router
from routers.currency import router as currency_router
from routers.metal import router as metal_router
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


async def _asset_not_found_handler(request: Request, exc: Exception):
    logger.warning("Asset not found on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Asset not found"},
    )


async def _holding_not_found_handler(request: Request, exc: Exception):
    logger.warning("Holding not found on %s %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Holding not found"},
    )


async def _unknown_currency_handler(request: Request, exc: Exception):
    logger.warning("Unknown currency on %s %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Currency not found"},
    )


async def _transaction_not_found_handler(request: Request, exc: Exception):
    logger.warning("Transaction not found on %s %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Transaction not found"},
    )


async def _insufficient_amount_handler(request: Request, exc: Exception):
    logger.warning("Uncovered sell on %s %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Not enough of this asset held"},
    )


async def _upstream_timeout_handler(request: Request, exc: Exception):
    logger.error("Upstream timeout on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": "External service timeout"},
    )


async def _upstream_error_handler(request: Request, exc: Exception):
    logger.error("Upstream error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "External service unavailable"},
    )


app.add_exception_handler(HoldingNotFound, _holding_not_found_handler)
app.add_exception_handler(UnknownCurrency, _unknown_currency_handler)
app.add_exception_handler(OperationalError, _database_unavailable_handler)
app.add_exception_handler(InterfaceError, _database_unavailable_handler)
app.add_exception_handler(AssetNotFound, _asset_not_found_handler)
app.add_exception_handler(UpstreamTimeout, _upstream_timeout_handler)
app.add_exception_handler(UpstreamError, _upstream_error_handler)
app.add_exception_handler(InsufficientHoldingAmount, _insufficient_amount_handler)
app.add_exception_handler(TransactionNotFound, _transaction_not_found_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metal_router)
app.include_router(crypto_router)
app.include_router(stock_router)
app.include_router(currency_router)
app.include_router(auth_router)
app.include_router(portfolio_router)
