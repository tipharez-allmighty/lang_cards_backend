from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

import src.decks.models
import src.flashcards.models
import src.users.models
from src.database import db_init
from src.decks.router import router as decks_router
from src.flashcards.router import router as flashcards_router
from src.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_init()
    yield


app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(decks_router)
api_router.include_router(flashcards_router)
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
