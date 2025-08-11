from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import AsyncClient

from src.database import get_session, get_supabase_client
from src.decks.service import deck_generator

router = APIRouter(prefix="/decks", tags=["Decks"])


@router.get("/stream")
async def stream_deck_progress(
    request: Request,
    db: AsyncSession = Depends(get_session),
    supabase: AsyncClient = Depends(get_supabase_client),
    user_id: UUID = uuid4(),
    user_input: str = "你好，世界",
    native_lang: str = "en",
):
    return StreamingResponse(
        deck_generator(request, db, supabase, user_id, user_input, native_lang),
        media_type="text/event-stream",
    )
