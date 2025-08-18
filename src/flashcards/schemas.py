from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    id: UUID
    url: str

    model_config = ConfigDict(from_attributes=True)


class WordBase(BaseModel):
    id: UUID
    word: str
    image: ImageBase

    model_config = ConfigDict(from_attributes=True)


class FlashCardBase(BaseModel):
    id: UUID
    native_lang: str
    target_lang: str
    data: dict
    created_at: datetime
    word: WordBase

    model_config = ConfigDict(from_attributes=True)
