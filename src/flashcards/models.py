import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import Base
from src.decks.models import decks_flashcards_table


class FlashCard(Base):
    __tablename__ = "flashcards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )

    word_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )
    native_lang: Mapped[str] = mapped_column(String(35), nullable=False)
    target_lang: Mapped[str] = mapped_column(String(35), nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    word: Mapped["Word"] = relationship(
        "Word", back_populates="flashcards", passive_deletes=True
    )
    decks: Mapped[list["Deck"]] = relationship(
        "Deck", secondary=decks_flashcards_table, back_populates="flashcards"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, word={self.word}, lang_pair={self.native_lang}-{self.target_lang})>"


class Word(Base):
    __tablename__ = "words"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )

    word: Mapped[str] = mapped_column(Text, nullable=False)

    image: Mapped["Image"] = relationship(
        "Image", back_populates="words", lazy="joined", passive_deletes=True
    )
    flashcards: Mapped[list[FlashCard]] = relationship(
        "FlashCard", back_populates="word", cascade="all, delete"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, word={self.word})>"


class Image(Base):
    __tablename__ = "images"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    path: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    words: Mapped[list["Word"]] = relationship(
        "Word", back_populates="image", cascade="all, delete"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, word={self.url})>"
