import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database import Base

profiles_decks_table = Table(
    "profiles_decks",
    Base.metadata,
    Column(
        "profile_id", UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True
    ),
    Column("deck_id", UUID(as_uuid=True), ForeignKey("decks.id"), primary_key=True),
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
        "Deck", secondary=profiles_decks_table, back_populates="profiles"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"
