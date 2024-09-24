from app.storyteller.story_item_retrievers import StoryItemRetrievers
from app.storyteller.storyteller_schemas import StoryContext


class SettingManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.story_excerpt: str = story_excerpt
        self.retriever: StoryItemRetrievers = StoryItemRetrievers()

    async def handle_setting_changes(self) -> None:
        await self.handle_location_changes()
        await self.handle_narration_changes()
        await self.handle_theme_changes()
        await self.handle_timeline_changes()

    async def handle_location_changes(self) -> None:
        ## Location changes
        ## Weather changes
        pass

    async def handle_narration_changes(self) -> None:
        ## Narrator changes
        ## Narration rules changes
        pass

    async def handle_theme_changes(self) -> None:
        ## Theme changes
        pass

    async def handle_timeline_changes(self) -> None:
        ## Timeline changes
        pass
