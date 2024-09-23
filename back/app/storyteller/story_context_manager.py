import json

from app.storyteller.ai_query import AiQuery
from app.storyteller.story_item_retrievers import StoryItemRetrievers, StoryItemUpdater
from app.storyteller.storyteller_schemas import (
    Character,
    CharacterEnteringLeavingResponse,
    CharacterNameAndId,
    CurrentContextSummaryData,
    EnteringCharacterResponse,
    StoryContext,
)
from app.utils.loggers import story_logger as log


class StoryPrompts:
    @staticmethod
    def sys_instruct() -> str:
        return """You are an assistant executing tasks to help in the maintenance of a story."""

    @staticmethod
    def leaving_entering_prompt() -> str:
        return """Look at the excerpt and determine if any characters are leaving or
        entering the scene, if they are respond true in the leaving and/or entering field."""

    @staticmethod
    def leaving_prommpt(characters: list[CharacterNameAndId], story_excerpt: str) -> str:
        return f""" Identify which of the following characters are leaving the scene in
        the passage \n The characters: \n
        {characters}
        The passage: \n {story_excerpt} \n
        return their names and ids as per the provided format"""

    @staticmethod
    def entering_character_prompt(
        existing_characters: list[CharacterNameAndId],
        story_excerpt: str,
    ) -> str:
        return f"""Here is a list of all the characters in the story:
        {existing_characters}, identify if any of these characters are entering
        the scene or if any new ones are appearing in the following passage: \n
        {story_excerpt} \n, if they are existing characters respond with
        their name and id,
        if they are new characters respond with their name and a new unique id"""

    @staticmethod
    def new_character_prompt(story_excerpt: str, char: CharacterNameAndId) -> str:
        return f"""A new character was introduced to a story from the following
        passage {story_excerpt}, fill in the character details with the characters'
        for the character with id {char.characterId} and name {char.name}, only fill
        in the fields that are clear from the passage, for other fields use an empty string"""

    @staticmethod
    def identify_character_changes(story_excerpt: str, char_list) -> str:
        return f"""Identify whether any of the following characters {char_list} underwent any
        changes in the following excerpt {story_excerpt}. Return whether characters have changed
        or not and Return a list of character Ids,
        their names and the changes according to the format provided"""


class StoryContextManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.character_manager: CharacterManager = CharacterManager(context, story_excerpt)
        self.plot_manager: PlotManager = PlotManager(context, story_excerpt)
        self.setting_manager: SettingManager = SettingManager(context, story_excerpt)
        self.retriever = StoryItemRetrievers()

    def update_story_excerpt(self, story_excerpt: str) -> None:
        self.character_manager.story_excerpt = self.plot_manager.story_excerpt = (
            self.setting_manager.story_excerpt
        ) = story_excerpt

    # TODO: Consider add more depth, for example looking up the characters involve in the plots
    async def create_context_summary(self) -> None:
        self.current_context_summary_data: CurrentContextSummaryData
        self.set_main_plot()
        self.set_sub_plot()
        self.set_characters_present()
        self.set_narrator()
        self.current_context_summary_data.themes = self.retriever.retrieve_themes(self.context)
        self.current_context_summary_data.location = self.context.currentContext.location
        self.current_context_summary_data.time = self.context.currentContext.time
        self.current_context_summary_data.weather = self.context.currentContext.weather
        await self.create_context_description()

    def set_main_plot(self) -> None:
        if self.context.currentContext.mainPlot:
            main_plot = self.retriever.retrieve_main_plot_point_data(
                self.context,
                self.context.currentContext.mainPlot,
            )
            if main_plot:
                self.current_context_summary_data.mainPlot = main_plot

    def set_sub_plot(self) -> None:
        if self.context.currentContext.subPlot:
            sub_plot = self.retriever.retrieve_secondary_plot_point_data(
                self.context,
                self.context.currentContext.subPlot,
            )
            if sub_plot:
                self.current_context_summary_data.subPlot = sub_plot

    def set_characters_present(self) -> None:
        if self.context.currentContext.charactersPresent:
            for character_name_and_id in self.context.currentContext.charactersPresent:
                main_characters = self.retriever.retrieve_main_character_data(
                    self.context,
                    character_name_and_id.characterId,
                )
                if main_characters:
                    self.current_context_summary_data.mainCharacters.append(main_characters)
                secondary_characters = self.retriever.retrieve_secondary_character_data(
                    self.context,
                    character_name_and_id.characterId,
                )
                if secondary_characters:
                    self.current_context_summary_data.secondaryCharacters.append(
                        secondary_characters,
                    )

    def set_narrator(self) -> None:
        if self.context.currentContext.Narator:
            narrator = self.retriever.retrieve_narrator_data(
                self.context,
                self.context.currentContext.Narator,
            )
            if narrator:
                self.current_context_summary_data.Narator = narrator

    async def create_context_description(self) -> str:
        dumped_context = self.current_context_summary_data.model_dump()
        context_str = json.dumps(dumped_context, indent=1)
        sys_instruct = """Use the data to create a description of the current state of the story.
        Respond with the description and only that."""
        ai_query = AiQuery("", "")
        response = await ai_query.query_gpt_general(context_str, sys_instruct)
        description = response.choices[0].message.content
        log.info(description)
        return description


class CharacterManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.story_excerpt: str = story_excerpt
        self.ai_query: AiQuery = AiQuery("gpt", self.story_excerpt)
        self.retriever: StoryItemRetrievers = StoryItemRetrievers()
        self.updater: StoryItemUpdater = StoryItemUpdater()

    async def handle_character_changes(self) -> None:
        self.add_existing_characters_to_list()

        await self.handle_characters_leaving_and_entering()
        await self.update_existing_characters()

    def add_existing_characters_to_list(self) -> None:
        characters = self.retriever.retrieve_list_of_all_characters_in_story(self.context)
        self.existing_characters = "".join([str(char.model_dump()) for char in characters])

    async def handle_characters_leaving_and_entering(self) -> None:
        assist_content = StoryPrompts.leaving_entering_prompt()
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content,
            sys_content,
            CharacterEnteringLeavingResponse,
        )
        if response.choices[0].message.parsed.leaving:
            await self.leaving_character()
        if response.choices[0].message.parsed.entering:
            await self.entering_character()

    async def update_existing_characters(self) -> None:
        assist_content = StoryPrompts.identify_character_changes(
            self.story_excerpt,
            self.existing_characters,
        )

    async def update_existing_character(self) -> None:
        pass

    async def leaving_character(self) -> None:
        assist_content = StoryPrompts.leaving_prommpt(
            self.context.currentContext.charactersPresent,
            self.story_excerpt,
        )

        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content,
            sys_content,
            CharacterEnteringLeavingResponse,
        )
        if response.choices[0].message.parsed.characters:
            for char in response.choices[0].message.parsed.characters:
                character = self.retriever.retrieve_main_character_data(
                    self.context,
                    char.characterId,
                )
                if character:
                    self.updater.remove_character_from_current_context(self.context, character.id)

    async def entering_character(self) -> None:
        ### confirms there are characters entering
        ### Need to identify if they are new characters or existing ones
        ### Retrieve list of all characters, and ask LLM if this is one of the characters entering
        ### if so response with character id and name
        ### if not create new character and add to context
        assist_content = StoryPrompts.entering_character_prompt(
            self.existing_characters,
            self.story_excerpt,
        )
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content,
            sys_content,
            EnteringCharacterResponse,
        )
        if response.choices[0].message.parsed.existing_characters:
            for char in response.choices[0].message.parsed.existing_characters:
                character = self.retriever.retrieve_main_character_data(
                    self.context,
                    char.characterId,
                )
                if character:
                    self.updater.add_character_to_current_context(self.context, character)
        if response.choices[0].message.parsed.new_characters:
            for char in response.choices[0].message.parsed.new_characters:
                await self.create_new_character(char)

    async def create_new_character(self, char: CharacterNameAndId) -> None:
        assist_content = StoryPrompts.new_character_prompt(self.story_excerpt, char)
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(assist_content, sys_content, Character)
        if response.choices[0].message.parsed:
            new_character = Character(**response.choices[0].message.parsed)
            self.updater.add_new_character_to_context(self.context, new_character)


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


class SettingManager:
    def __init__(self, context: StoryContext, story_excerpt: str) -> None:
        self.context: StoryContext = context
        self.story_excerpt: str = story_excerpt
        self.retriever: StoryItemRetrievers = StoryItemRetrievers()

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
