from datetime import datetime
from uuid import UUID
from enum import StrEnum

from pydantic import BaseModel, ConfigDict
from taskiq.depends.progress_tracker import TaskState
from src.flashcards.schemas import FlashCardBase


class DeckBase(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    flashcards: list[FlashCardBase]

    model_config = ConfigDict(from_attributes=True)


class Task(BaseModel):
    id: str


class TaskResult(BaseModel):
    status: TaskState
    result: DeckBase | None = None
