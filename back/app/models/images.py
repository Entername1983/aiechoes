from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base


class Images(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True)
    img_model: Mapped[str] = mapped_column(String(30), nullable=False)
    time_created: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(),
    )
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "title": self.title,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "img_model": self.img_model,
            "time_created": self.time_created,
            "story_id": self.story_id,
        }
