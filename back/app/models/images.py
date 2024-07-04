from datetime import datetime
from sqlalchemy import DateTime,Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.config.db import Base


class Images(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=True)
    time_created: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now()
    )