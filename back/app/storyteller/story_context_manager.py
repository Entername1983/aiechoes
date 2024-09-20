import json

from app.storyteller.ai_query import AiQuery
from app.storyteller.storyteller_schemas import (
    Character,
    CurrentContext,
    CurrentContextSummaryData,
    Narrator,
    PlotPoint,
    Rules,
    StoryContext,
)


class StoryContextManager:
    def __init__(self, context: StoryContext):
        self.context: StoryContext = context

    def retrieve_main_character_data(self, character_id: str) -> Character | None:
        return next(
            (char for char in self.context.characters.mainCharacters if char.id == character_id),
            None,
        )

    def retrieve_secondary_character_data(self, character_id: str) -> Character | None:
        return next(
            (
                char
                for char in self.context.characters.secondaryCharacters
                if char.id == character_id
            ),
            None,
        )

    def retrieve_main_plot_point_data(self, plot_id: str) -> PlotPoint | None:
        return next(
            (plot for plot in self.context.mainPlots if plot.id == plot_id),
            None,
        )

    def retrieve_secondary_plot_point_data(self, plot_id: str) -> PlotPoint | None:
        return next(
            (plot for plot in self.context.subPlots if plot.id == plot_id),
            None,
        )

    def retrieve_rules(self) -> Rules:
        return self.context.rules

    def retrieve_themes(self) -> list[str]:
        return self.context.themes

    def retrieve_narrator_data(self, narrator_id: str) -> Narrator | None:
        return next(
            (narrator for narrator in self.context.narration if narrator.id == narrator_id),
            None,
        )

    def retrieve_current_context(self) -> CurrentContext:
        return self.context.currentContext

    # TODO: Consider add more depth, for example looking up the characters involve in the plots
    async def create_context_summary(self) -> None:
        self.current_context_summary_data: CurrentContextSummaryData
        if self.context.currentContext.mainPlot is not None:
            self.current_context_summary_data.mainPlot = self.retrieve_main_plot_point_data(
                self.context.currentContext.mainPlot,
            )
        if self.context.currentContext.subPlot is not None:
            self.current_context_summary_data.subPlot = self.retrieve_secondary_plot_point_data(
                self.context.currentContext.subPlot,
            )
        if self.context.currentContext.charactersPresent is not None:
            for character_id in self.context.currentContext.charactersPresent:
                self.current_context_summary_data.mainCharacters.append(
                    self.retrieve_main_character_data(character_id),
                )
                self.current_context_summary_data.secondaryCharacters.append(
                    self.retrieve_secondary_character_data(character_id),
                )

        if self.context.currentContext.Narator is not None:
            self.current_context_summary_data.Narator = self.retrieve_narrator_data(
                self.context.currentContext.Narator,
            )
        self.current_context_summary_data.themes = self.retrieve_themes()
        self.current_context_summary_data.location = self.context.currentContext.location
        self.current_context_summary_data.time = self.context.currentContext.time
        self.current_context_summary_data.weather = self.context.currentContext.weather
        await self.create_context_description()

    async def create_context_description(self) -> str:
        dumped_context = self.current_context_summary_data.model_dump()
        context_str = json.dumps(dumped_context, indent=1)
        sys_instruct = """Use the data to create a description of the current state of the story.
        Respond with the description and only that."""
        ai_query = AiQuery("", "")
        description = await ai_query.query_gpt_general(context_str, sys_instruct)
        print(description)
        return description
