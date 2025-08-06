import asyncio

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import AsyncClient

from src.core.llm import image_generation, text_generation
from src.flashcards.image_storage import get_image_url, remove_images, upload_image
from src.flashcards.models import FlashCard, Image, Word


async def get_image(db: AsyncSession, word: str) -> Image | None:
    image = await db.execute(
        select(Image).join(Word, Word.image_id == Image.id).where(Word.word == word)
    )

    return image.scalar_one_or_none()


async def get_or_create_image_with_word(
    db: AsyncSession, supabase: AsyncClient, word: str
) -> Word:
    image = await get_image(db, word)
    if image:
        return image
    image_bytes = await image_generation(word)
    if not image_bytes:
        raise ValueError(f"No image generated for {word}")
    image_path = await upload_image(supabase, image_bytes)
    image_url = await get_image_url(supabase, image_path)

    new_image = Image(path=image_path, url=image_url)

    try:
        db.add(new_image)
        await db.flush()

        new_word = Word(word=word, image=new_image)

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
    db: AsyncSession,
    supabase: AsyncClient,
    word: str,
    target_lang: str,
    native_lang: str,
) -> FlashCard:
    text_data = asyncio.create_task(text_generation(word, target_lang, native_lang))
    word_with_image_data = asyncio.create_task(
        get_or_create_image_with_word(db, supabase, word)
    )

    text_result, word_with_image_result = await asyncio.gather(
        text_data, word_with_image_data
    )
    new_word = Word(
        word=text_result.word_translation, image=word_with_image_result.image
    )

    try:
        db.add(new_word)

        flash_card = FlashCard(
            word=word_with_image_result,
            native_lang=native_lang,
            target_lang=target_lang,
            data=text_result.model_dump(),
        )

        db.add(flash_card)

        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    return flash_card
