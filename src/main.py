from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

import src.decks.models
import src.flashcards.models
import src.users.models
from src.database import db_init
from src.decks.router import router as decks_router
from src.flashcards.router import router as flashcards_router
from src.users.router import router as users_router
from src.broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    if not broker.is_worker_process():
        await broker.startup()
    yield
    if not broker.is_worker_process():
        await broker.shutdown()


app = FastAPI(lifespan=lifespan, root_path="/api")

app.include_router(users_router)
app.include_router(decks_router)
app.include_router(flashcards_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
