from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    datetime_found: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__}(id={self.id}"
        )
