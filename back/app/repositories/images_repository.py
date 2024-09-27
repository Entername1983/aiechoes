from sqlalchemy import desc, select

from app.dependencies.db import AsyncSession
from app.models.models import Images


class ImagesRepository:
    @staticmethod
    async def retrieve_image_from_db_by_story_id_and_batch_id(
        db: AsyncSession, story_id: int, batch_id: int
    ) -> Images | None:
        result = await db.execute(
            select(Images)
            .filter(Images.story_id == story_id)
            .filter(Images.batch_id == batch_id)
            .order_by(desc(Images.id))
            .limit(1)
        )
        return result.scalars().first()
