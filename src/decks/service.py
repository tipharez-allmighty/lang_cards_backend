import asyncio

from src.core.llm import image_generation, text_generation, words_list_generation
from src.core.schemas import FlashCardLLMOut


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
