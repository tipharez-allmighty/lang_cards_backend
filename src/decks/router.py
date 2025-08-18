from uuid import UUID, uuid4

from fastapi import APIRouter, Depends

from src.database import get_session, get_supabase_client
from src.decks.schemas import DeckBase
from src.decks.service import create_deck
from supabase import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.post("/", response_model=DeckBase)
async def generate_deck(
    db: AsyncSession = Depends(get_session),
    supabase: AsyncClient = Depends(get_supabase_client),
    user_id: UUID = uuid4(),
    user_input: str = "你好，世界",
    native_lang: str = "en",
) -> DeckBase:
    deck = await create_deck(db, supabase, user_id, user_input, native_lang)
    return DeckBase.model_validate(deck)
