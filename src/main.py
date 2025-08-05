from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import db_init
from src.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
