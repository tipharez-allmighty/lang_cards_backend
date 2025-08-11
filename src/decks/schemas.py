from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.flashcards.schemas import FlashCardBase

class DeckBase(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    flashcards: list[FlashCardBase]

    class Config:
        from_attributes = True