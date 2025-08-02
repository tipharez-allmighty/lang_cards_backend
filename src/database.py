from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.models import Base

engine = create_async_engine(
    url=(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )
)
async_session = async_sessionmaker(engine)


async def db_init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
        
@asynccontextmanager
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
