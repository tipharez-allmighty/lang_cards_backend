import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func

Base = declarative_base()

profile_decks_table = Table(
    "profiles_decks",
    Base.metadata,
    Column(
        "profile_id", UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True
    ),
    Column("deck_id", UUID(as_uuid=True), ForeignKey("decks.id"), primary_key=True),
)

deck_flashcard_table = Table(
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


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    role: Mapped[str] = mapped_column(
        Enum("admin", "teacher", "user", name="role_enum"),
        nullable=False,
        default="user",
    )

    decks: Mapped[list["Deck"]] = relationship(
        "Deck", secondary=profile_decks_table, back_populates="profiles"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)

    flashcards: Mapped[list["FlashCard"]] = relationship(
        "FlashCard", secondary=deck_flashcard_table, back_populates="decks"
    )
    profiles: Mapped[list["Profile"]] = relationship(
        "Profile", secondary=profile_decks_table, back_populates="decks"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, title={self.title})>"


class FlashCard(Base):
    __tablename__ = "flashcards"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )

    word: Mapped[str] = mapped_column(Text, nullable=False)
    native_lang: Mapped[str] = mapped_column(String(35), nullable=False)
    target_lang: Mapped[str] = mapped_column(String(35), nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    image: Mapped["Image"] = relationship("Image", back_populates="flashcards")
    decks: Mapped[list["Deck"]] = relationship(
        "Deck", secondary=deck_flashcard_table, back_populates="flashcards"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, word={self.word}, lang_pair={self.native_lang}-{self.target_lang})>"


class Image(Base):
    __tablename__ = "images"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    word: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    flashcards: Mapped[list[FlashCard]] = relationship(
        "FlashCard", back_populates="image"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, word={self.word})>"
