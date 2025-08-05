from pydantic import BaseModel


class WordsList(BaseModel):
    language: str | None = None
    title: str | None = None
    words: list[str] | None = None


class Sentences(BaseModel):
    sentence: str
    sentence_romanization: str
    sentence_translation: str


class FlashCardLLM(BaseModel):
    hint: str
    word: str
    word_romanization: str
    word_translation: str
    sentences: list[Sentences]


class FlashCardLLMOut(FlashCardLLM):
    image: bytes
