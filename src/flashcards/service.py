import asyncio

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload
from supabase import AsyncClient

from src.core.llm import image_generation, text_generation
from src.database import get_db
from src.exceptions import LLMResponseError
from src.flashcards.image_storage import get_image_url, remove_images, upload_image
from src.flashcards.models import FlashCard, Image, Word


async def get_image(db: AsyncSession, word: str) -> Image | None:
    result = await db.execute(
        select(Image).join(Word, Word.image_id == Image.id).where(Word.word == word)
    )

    return result.scalar_one_or_none()


async def get_word(db: AsyncSession, word: str) -> Word:
    result = await db.execute(
        select(Word).options(noload(Word.image)).where(Word.word == word)
    )

    return result.scalar_one_or_none()


async def get_word_with_image(db: AsyncSession, word: str):
    result = await db.execute(select(Word).where(Word.word == word))

    return result.scalar_one_or_none()


async def get_or_create_image_with_word(
    db: AsyncSession, supabase: AsyncClient, word: str
) -> Word:
    existing_word = await get_word_with_image(db, word)
    if existing_word:
        return existing_word
    image_bytes = await image_generation(word)
    if not image_bytes:
        raise LLMResponseError(f"No image generated for {word}")
    image_path = await upload_image(supabase, image_bytes)
    image_url = await get_image_url(supabase, image_path)

    new_image = Image(path=image_path, url=image_url)
    new_word = Word(word=word, image=new_image)

    try:
        db.add(new_image)
        db.add(new_word)
        await db.commit()
        await db.refresh(new_image)
        await db.refresh(new_word)
    except SQLAlchemyError as e:
        await db.rollback()
        failed_deletions = await remove_images(supabase, [image_path])
        if not failed_deletions:
            raise e
        raise SQLAlchemyError(
            f"{e}\nFailed to delete images from Supabase storage: {failed_deletions}"
        )
    return new_word


async def create_flashcard(
    supabase: AsyncClient,
    word: str,
    target_lang: str,
    native_lang: str,
) -> FlashCard:
    text_data = asyncio.create_task(text_generation(word, target_lang, native_lang))

    async with get_db() as db:
        word_with_image_data = asyncio.create_task(
            get_or_create_image_with_word(db, supabase, word)
        )

        text_result, word_with_image_result = await asyncio.gather(
            text_data, word_with_image_data
        )
        translated_word = await get_word(db, text_result.word_translation)

        try:
            if not translated_word:
                new_word = Word(
                    word=text_result.word_translation,
                    image=word_with_image_result.image,
                )
                db.add(new_word)
            flash_card = FlashCard(
                word=word_with_image_result,
                native_lang=native_lang,
                target_lang=target_lang,
                data=text_result.model_dump(),
            )

            db.add(flash_card)

            await db.commit()
            await db.refresh(flash_card)
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return flash_card


async def get_flash_cards_by_list(
    db: AsyncSession, target_lang: str, native_lang: str, word_list: list[str]
) -> tuple[list[FlashCard], list[str]]:
    flashcards = await db.execute(
        select(FlashCard)
        .join(FlashCard.word)
        .where(
            and_(
                FlashCard.target_lang == target_lang,
                FlashCard.native_lang == native_lang,
                Word.word.in_(word_list),
            )
        )
    )
    found_flashcards = list(flashcards.scalars().all())
    missing_words = []
    if len(found_flashcards) < len(word_list):
        found_words = {flashcard.word.word for flashcard in found_flashcards}
        word_set = set(word_list)
        missing_words = list(word_set - found_words)
    return found_flashcards, missing_words
