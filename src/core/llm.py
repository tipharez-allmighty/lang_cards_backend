import asyncio
import random
from io import BytesIO

from google import genai
from google.genai import types
from mirascope import llm
from PIL import Image
from pydantic import BaseModel

from src.config import settings
from src.core.prompts import IMAGE_PROMPT, WORD_CARD_PROMPT, WORDS_LIST_PROMPT
from src.core.schemas import FlashCardLLM, FlashCardLLMOut, WordsList

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


async def image_generation(word: str):
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


async def get_card(word: str, target_lang: str, native_lang: str):
    card_text = asyncio.create_task(text_generation(word, target_lang, native_lang))
    card_image = asyncio.create_task(image_generation(word))

    text_result, image_result = await asyncio.gather(card_text, card_image)
    if not text_result:
        print("NO TEXT")
    if not image_result:
        print("NO IMAGE")
    return FlashCardLLMOut(**text_result.model_dump(), image=image_result)


async def main(input: str, native_lang):
    words_list = await words_list_generation(input)
    if words_list.language is None:
        raise Exception("String is invalid. Use same language for all the words.")

    print(words_list.language)
    tasks = [
        asyncio.create_task(get_card(word, words_list.language, native_lang))
        for word in words_list.words
    ]

    results = await asyncio.gather(*tasks)
    print(words_list.title)
    print(
        [(word_card.word, word_card.hint, word_card.sentences) for word_card in results]
    )


if __name__ == "__main__":
    asyncio.run(main(input="This is a car and this is the train", native_lang="en"))
