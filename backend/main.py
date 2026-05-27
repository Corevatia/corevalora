import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.crypto import router as crypto_router
from routers.stock import router as stock_router
from routers.currency import router as currency_router
from routers.auth import router as auth_router
from routers.portfolio import router as portfolio_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.logging_config import setup_logging
from core.rate_limit import limiter
from db.database import SessionLocal
from services.auth.sessions import delete_expired_sessions

setup_logging()
logger = logging.getLogger(__name__)

SESSION_CLEANUP_INTERVAL_SECONDS = 60 * 60 * 6


async def _session_cleanup_loop():
    while True:
        try:
            with SessionLocal() as db:
                deleted = delete_expired_sessions(db)
                if deleted:
                    logger.info("Deleted %d expired sessions", deleted)
        except Exception:
            logger.exception("Session cleanup failed")
        await asyncio.sleep(SESSION_CLEANUP_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_session_cleanup_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="CoreValora", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crypto_router)
app.include_router(stock_router)
app.include_router(currency_router)
app.include_router(auth_router)
app.include_router(portfolio_router)