from fastapi import FastAPI
from routers.crypto import router as crypto_router
from routers.stock import router as stock_router
from routers.currency import router as currency_router
from routers.auth import router as auth_router
from routers.portfolio import router as portfolio_router
from fastapi.middleware.cors import CORSMiddleware
from core.logging_config import setup_logging

app = FastAPI(title="CoreValora")
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

setup_logging()
