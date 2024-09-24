from app.storyteller.story_item_retrievers import StoryItemRetrievers
from app.storyteller.storyteller_schemas import StoryContext


class PlotManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.story_excerpt: str = story_excerpt
        self.retriever: StoryItemRetrievers = StoryItemRetrievers()

    async def handle_plot_changes(self) -> None:
        ## Plot changes
        ## new dependencies
        ## new related subplots
        ## new status
        pass
