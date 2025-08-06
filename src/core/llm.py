import asyncio
import random
from io import BytesIO

from google import genai
from google.genai import types
from mirascope import llm
from PIL import Image

from src.config import settings
from src.core.prompts import IMAGE_PROMPT, WORD_CARD_PROMPT, WORDS_LIST_PROMPT
from src.core.schemas import FlashCardLLM, WordsList

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)


@llm.call(
    client=gemini_client,
    provider="google",
    model=settings.GOOGLE_TEXT_LITE,
    response_model=WordsList,
)
async def words_list_generation(words: str):
    return WORDS_LIST_PROMPT.format(words=words)


@llm.call(
    client=gemini_client,
    provider="google",
    model=settings.GOOGLE_TEXT_LITE,
    response_model=FlashCardLLM,
)
async def text_generation(word: str, target_lang, native_lang: str):
    return WORD_CARD_PROMPT.format(
        word=word, target_lang=target_lang, native_lang=native_lang
    )


async def image_generation(word: str) -> bytes | None:
    response = await gemini_client.aio.models.generate_content(
        model=settings.GOOGLE_IMAGE,
        contents=IMAGE_PROMPT.format(word=word),
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f"{word}-{random.randint(1, 1000)}.png")
            # image.show()
            # buffer = BytesIO()
            # image.save(buffer, format="PNG")
            # base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return part.inline_data.data
    return None
