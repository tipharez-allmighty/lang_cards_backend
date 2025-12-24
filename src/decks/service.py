import asyncio
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import AsyncClient

from src.core.llm import word_list_generation
from src.decks.models import Deck
from src.flashcards.models import FlashCard
from src.flashcards.service import create_flashcard, get_flash_cards_by_list
from src.users.service import get_profile_by_id


async def upload_deck(
    db: AsyncSession, user_id: UUID, title: str, flashcards: list[FlashCard]
) -> Deck:
    profile = await get_profile_by_id(db, user_id)
    try:
        new_deck = Deck(title=title, flashcards=flashcards)
        if profile:
            new_deck.profiles.append(profile)

        db.add(new_deck)

        await db.commit()
        await db.refresh(new_deck)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

    return new_deck


async def create_deck(
    db: AsyncSession,
    supabase: AsyncClient,
    user_id: UUID,
    user_input: str,
    native_lang: str,
):
    word_list = await word_list_generation(user_input)

    flashcards, missing_words = await get_flash_cards_by_list(
        db,
        target_lang=word_list.language,
        native_lang=native_lang,
        word_list=word_list.words,
    )

    if missing_words:
        tasks = [
            asyncio.create_task(
                create_flashcard(
                    supabase=supabase,
                    word=word,
                    target_lang=word_list.language,
                    native_lang=native_lang,
                )
            )
            for word in missing_words
        ]

        new_flashcards = await asyncio.gather(*tasks)
        flashcards.extend(new_flashcards)

    return await upload_deck(db, user_id, word_list.title, flashcards)
