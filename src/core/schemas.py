from pydantic import BaseModel, model_validator

from src.exceptions import LLMResponseError


class WordList(BaseModel):
    language: str | None = None
    title: str
    words: list[str] | None = None

    @model_validator(mode="after")
    def check_llm_response(self):
        errors = []
        if self.language is None or self.language == "null":
            errors.append(
                "Invalid user input: please use the same language for all words."
            )
        if self.words is None:
            errors.append("LLM failed to generate list of words.")

        if errors:
            raise LLMResponseError(" | ".join(errors))

        return self


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
