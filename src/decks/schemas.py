from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.flashcards.schemas import FlashCardBase


class DeckBase(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    flashcards: list[FlashCardBase]

    model_config = ConfigDict(from_attributes=True)
