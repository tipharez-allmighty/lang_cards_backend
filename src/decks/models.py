import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import Base
from src.users.models import profiles_decks_table

decks_flashcards_table = Table(
    "decks_flashcards",
    Base.metadata,
    Column("deck_id", UUID(as_uuid=True), ForeignKey("decks.id"), primary_key=True),
    Column(
        "flashcard_id",
        UUID(as_uuid=True),
        ForeignKey("flashcards.id"),
        primary_key=True,
    ),
)


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    flashcards: Mapped[list["FlashCard"]] = relationship(
        "FlashCard",
        secondary=decks_flashcards_table,
        back_populates="decks",
        lazy="selectin",
    )
    profiles: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary=profiles_decks_table,
        back_populates="decks",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, title={self.title})>"
