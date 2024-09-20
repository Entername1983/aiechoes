from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base


class StoryContexts(Base):
    __tablename__ = "story_contexts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer, nullable=False)
    context: Mapped[dict] = mapped_column(JSONB, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "context": self.context,
        }
