from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base


class Replies(Base):
    __tablename__ = "replies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_created: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(),
    )
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    reply: Mapped[str] = mapped_column(String(512), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    batch_id: Mapped[int] = mapped_column(Integer, nullable=False)
    number_in_batch: Mapped[int] = mapped_column(Integer, nullable=False)
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "time_created": self.time_created.isoformat()
            if isinstance(self.time_created, datetime)
            else self.time_created,
            "model": self.model,
            "reply": self.reply,
            "version": self.version if self.version else "not specified",
            "batch_id": self.batch_id,
            "number_in_batch": self.number_in_batch,
            "story_id": self.story_id,
        }
