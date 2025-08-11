import asyncio
from uuid import UUID

from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import AsyncClient

from src.core.llm import word_list_generation
from src.decks.models import Deck
from src.decks.schemas import DeckBase
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

        flashcards_tasks = asyncio.as_completed(tasks)
        counter = [len(flashcards), len(word_list.words)]
        async for task in flashcards_tasks:
            flashcard = await task
            flashcards.append(flashcard)
            counter[0] += 1
            yield counter

    yield await upload_deck(db, user_id, word_list.title, flashcards)


async def deck_generator(
    request: Request,
    db: AsyncSession,
    supabase: AsyncClient,
    user_id: UUID,
    user_input: str,
    native_lang: str,
):
    async for data in create_deck(
        db, supabase, user_id=user_id, user_input=user_input, native_lang=native_lang
    ):
        if isinstance(data, Deck):
            yield f"event: deck\ndata: {DeckBase.model_validate(data).model_dump_json()}\n\n"
        else:
            yield f"event: loading\ndata: {data}\n\n"
        if await request.is_disconnected():
            break
