import json

from app.storyteller.ai_query import AiQuery
from app.storyteller.story_item_retrievers import StoryItemRetrievers
from app.storyteller.story_section_managers.character_manager import CharacterManager
from app.storyteller.story_section_managers.plot_manager import PlotManager
from app.storyteller.story_section_managers.setting_manager import SettingManager
from app.storyteller.storyteller_schemas import CurrentContextSummaryData, StoryContext
from app.utils.loggers import story_logger as log


class StoryContextManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.character_manager: CharacterManager = CharacterManager(context, story_excerpt)
        self.plot_manager: PlotManager = PlotManager(context, story_excerpt)
        self.setting_manager: SettingManager = SettingManager(context, story_excerpt)
        self.retriever = StoryItemRetrievers()
        self.current_context_summary_data: CurrentContextSummaryData = CurrentContextSummaryData(
            mainCharacters=[], secondaryCharacters=[], themes=[]
        )

    def update_story_excerpt(self, story_excerpt: str) -> None:
        self.character_manager.story_excerpt = self.plot_manager.story_excerpt = (
            self.setting_manager.story_excerpt
        ) = story_excerpt

    async def update_story_context(self) -> None:
        await self.character_manager.handle_character_changes()
        self.context = self.plot_manager.context = self.setting_manager.context = (
            self.character_manager.context
        )
        await self.plot_manager.handle_plot_changes()
        self.context = self.character_manager.context = self.setting_manager.context = (
            self.plot_manager.context
        )
        await self.setting_manager.handle_setting_changes()
        self.context = self.character_manager.context = self.plot_manager.context = (
            self.setting_manager.context
        )

    # TODO: Consider add more depth, for example looking up the characters involve in the plots
    async def create_context_summary(self) -> str:
        self.set_main_plot()
        self.set_sub_plot()
        self.set_characters_present()
        self.set_narrator()
        self.current_context_summary_data.themes = self.retriever.retrieve_themes(self.context)
        if self.context.currentContext:
            self.current_context_summary_data.location = self.context.currentContext.location
            self.current_context_summary_data.time = self.context.currentContext.time
            self.current_context_summary_data.weather = self.context.currentContext.weather
        return await self.create_context_description()

    def set_main_plot(self) -> None:
        log.debug("-----------------SETTING MAIN PLOT-----------------\n --------------------")
        log.debug("-------------------------CONTEXT: %s", self.context)
        if self.context.currentContext and self.context.currentContext.mainPlot:
            main_plot = self.retriever.retrieve_main_plot_point_data(
                self.context, self.context.currentContext.mainPlot
            )
            log.debug("------------------MAIN PLOT: %s", main_plot)
            if main_plot:
                self.current_context_summary_data.mainPlot = main_plot

    def set_sub_plot(self) -> None:
        if self.context.currentContext and self.context.currentContext.subPlot:
            sub_plot = self.retriever.retrieve_secondary_plot_point_data(
                self.context, self.context.currentContext.subPlot
            )
            if sub_plot:
                self.current_context_summary_data.subPlot = sub_plot

    def set_characters_present(self) -> None:
        if self.context.currentContext and self.context.currentContext.charactersPresent:
            for character_name_and_id in self.context.currentContext.charactersPresent:
                main_characters = self.retriever.retrieve_main_character_data(
                    self.context, character_name_and_id.characterId
                )
                if main_characters:
                    self.current_context_summary_data.mainCharacters.append(main_characters)
                secondary_characters = self.retriever.retrieve_secondary_character_data(
                    self.context, character_name_and_id.characterId
                )
                if secondary_characters:
                    self.current_context_summary_data.secondaryCharacters.append(
                        secondary_characters
                    )

    def set_narrator(self) -> None:
        if self.context.currentContext and self.context.currentContext.narrator:
            narrator = self.retriever.retrieve_narrator_data(
                self.context, self.context.currentContext.narrator
            )
            if narrator:
                self.current_context_summary_data.narrator = narrator

    async def create_context_description(self) -> str:
        dumped_context = self.current_context_summary_data.model_dump()
        context_str = json.dumps(dumped_context, indent=1)
        log.info("CONTEXT STRING ------------------ %s", context_str)
        assis_content = f"""Here is a structured state of a the story, write a description of
        the current state based upon it.  The structure state {context_str}"""
        sys_instruct = """Use the data to create a description of the current state of the story.
        Respond with the description and only that."""
        ai_query = AiQuery("", "")
        response = await ai_query.query_gpt_general(assis_content, sys_instruct)
        description = response.choices[0].message.content
        log.info("---------------DESCRIPTION RETURNED ------------------ %s", description)
        return description
