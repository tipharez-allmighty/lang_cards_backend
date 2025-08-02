import logging
from fastapi import FastAPI

from src.router import router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
