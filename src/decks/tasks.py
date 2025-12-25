from uuid import UUID

from src.database import get_db, get_supabase_client
from src.broker import broker

from src.decks.schemas import DeckBase
from src.decks.service import create_deck


@broker.task
async def create_deck_task(user_id: UUID, user_input: str, native_lang: str):
    async with get_db() as db:
        deck = await create_deck(
            db=db,
            supabase=await get_supabase_client(),
            user_id=user_id,
            user_input=user_input,
            native_lang=native_lang,
        )
        return DeckBase.model_validate(deck)


@broker.task
async def create_test_deck_task(user_id: UUID, user_input: str, native_lang: str):
    import asyncio
    from src.decks.test_deck import data

    await asyncio.sleep(3)
    return DeckBase.model_validate(data)
