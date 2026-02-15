from fastapi import FastAPI
from app.routers.crypto import router as crypto_router

app = FastAPI(title="CoreValora")
app.include_router(crypto_router)