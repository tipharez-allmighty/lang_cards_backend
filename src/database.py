from contextlib import asynccontextmanager
from uuid import uuid4

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from supabase import AsyncClient, create_async_client

from src.config import settings
sdfsdf

engine = create_async_engine(
    url=(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    ),
    poolclass=NullPool,
    connect_args={
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
        "statement_cache_size": 0,
    },
)
async_session = async_sessionmaker(engine)

Base = declarative_base()


async def db_init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


async def get_supabase_client() -> AsyncClient:
    return await create_async_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


@asynccontextmanager
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
