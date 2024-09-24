from sqlalchemy import desc, select

from app.dependencies.db import AsyncSession
from app.models.models import StoryContexts
from app.storyteller.storyteller_schemas import StoryContext


class StoryContextRepository:
    @staticmethod
    async def retrieve_story_context(db: AsyncSession, story_id: int) -> StoryContexts:
        result = await db.execute(
            select(StoryContexts)
            .filter(StoryContexts.story_id == story_id)
            .order_by(desc(StoryContexts.id))
            .limit(1),
        )
        return result.scalars().first()

    @staticmethod
    async def add_new_context_entry_to_db(
        db: AsyncSession,
        story_context: StoryContext,
        story_id: int,
    ) -> None:
        context = story_context.model_dump()
        new_context = StoryContexts(story_id=story_id, context=context)
        db.add(new_context)
        await db.commit()
