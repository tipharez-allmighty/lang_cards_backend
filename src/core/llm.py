from google import genai
from google.genai import types
from mirascope import llm
from tenacity import retry, stop_after_attempt, wait_random_exponential

from src.config import settings
from src.core.prompts import IMAGE_PROMPT, WORD_CARD_PROMPT, WORD_LIST_PROMPT
from src.core.schemas import FlashCardLLM, WordList

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

llm_retry = retry(
    wait=wait_random_exponential(multiplier=0.5, max=2), stop=stop_after_attempt(3)
)


@llm_retry
@llm.call(
    client=gemini_client,
    provider="google",
    model=settings.GOOGLE_TEXT_LITE,
    response_model=WordList,
)
async def word_list_generation(words: str):
    return WORD_LIST_PROMPT.format(words=words)


@llm_retry
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


@llm_retry
async def image_generation(word: str) -> bytes | None:
    response = await gemini_client.aio.models.generate_content(
        model=settings.GOOGLE_IMAGE,
        contents=IMAGE_PROMPT.format(word=word),
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    return None
