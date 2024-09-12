from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base


class Replies(Base):
    __tablename__ = "replies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_created: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now()
    )
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    reply: Mapped[str] = mapped_column(String(512), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "time_created": self.time_created.isoformat()
            if isinstance(self.time_created, datetime)
            else self.time_created,
            "model": self.model,
            "reply": self.reply,
            "version": self.version if self.version else "not specified",
        }
