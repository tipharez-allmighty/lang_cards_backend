from uuid import UUID

from _pytest._code.code import ExceptionRepr

from src.database import get_db, get_supabase_client
from src.broker import broker

from src.decks.schemas import DeckBase
from src.decks.service import create_deck
from src.logger import logger


@broker.task
async def create_deck_task(user_id: UUID, user_input: str, native_lang: str):
    async with get_db() as db:
        logger.info("WE ARE IN THE TASK")
        deck = await create_deck(
            db=db,
            supabase=await get_supabase_client(),
            user_id=user_id,
            user_input=user_input,
            native_lang=native_lang,
        )
        logger.info("WTF IS GOING ON HERE")
        try:
            result = DeckBase.model_validate(deck)
        except Exception as e:
            logger.error(f"WTF {e}")
        logger.info(result)
        return DeckBase.model_validate(deck)
