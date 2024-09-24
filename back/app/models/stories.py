from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base


class Stories(Base):
    __tablename__ = "stories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    live: Mapped[bool] = mapped_column(Boolean, nullable=True)
    story_type: Mapped[str] = mapped_column(String(30), nullable=False)
    ## ec = excquisite corpse
    ## wc = with context

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "live": self.live,
            "story_type": self.story_type,
        }
