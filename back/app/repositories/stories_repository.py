from sqlalchemy import desc, select

from app.dependencies.db import AsyncSession
from app.models.models import Stories


class StoriesRepository:
    @staticmethod
    async def retrieve_story_by_id(db: AsyncSession, story_id: int) -> Stories:
        result = await db.execute(
            select(Stories).filter(Stories.id == story_id).order_by(desc(Stories.id)).limit(1),
        )
        return result.scalars().first()
