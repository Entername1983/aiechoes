from app.exceptions.StoryContextExceptions import StoryContextExceptions
from app.storyteller.ai_query import AiQuery
from app.storyteller.prompts import StoryPrompts
from app.storyteller.story_item_retrievers import StoryItemRetrievers, StoryItemUpdater
from app.storyteller.storyteller_schemas import (
    Character,
    CharacterEnteringLeavingResponse,
    CharacterNameAndId,
    EnteringCharacterResponse,
    StoryContext,
)
from app.utils.loggers import story_logger as log


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
            assist_content, sys_content, CharacterEnteringLeavingResponse
        )
        if not response.choices[0].message.parsed:
            raise StoryContextExceptions.NothingToParseError
        if response.choices[0].message.parsed.leaving:
            await self.leaving_character()
        if response.choices[0].message.parsed.entering:
            await self.entering_character()

    async def update_existing_characters(self) -> None:
        assist_content = StoryPrompts.identify_character_changes(
            self.story_excerpt, self.existing_characters
        )
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content, sys_content, CharacterEnteringLeavingResponse
        )
        if not response.choices[0].message.parsed:
            raise StoryContextExceptions.NothingToParseError
        if response.choices[0].message.parsed.charactersChanged:
            for char in response.choices[0].message.parsed.changes:
                character = self.retriever.retrieve_main_character_data(
                    self.context, char.characterId
                )
                if not character:
                    raise StoryContextExceptions.CharacterNotFoundError
                await self.get_updated_character_info(character, char.details)

    async def get_updated_character_info(self, character: Character, changes: str) -> None:
        char_string = str(character.model_dump())
        assist_content = StoryPrompts.update_character_info(char_string, changes)
        sys_instruct = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(assist_content, sys_instruct, Character)
        if response.choices[0].message.parsed:
            updated_character = Character(**response.choices[0].message.parsed)
            self.updater.update_existing_character_in_context(self.context, updated_character)

    async def leaving_character(self) -> None:
        if self.context.currentContext is None:
            raise StoryContextExceptions.NoCurrentContextError
        assist_content = StoryPrompts.leaving_prommpt(
            self.context.currentContext.charactersPresent, self.story_excerpt
        )

        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content, sys_content, CharacterEnteringLeavingResponse
        )
        if not response.choices[0].message.parsed:
            raise StoryContextExceptions.NothingToParseError
        if response.choices[0].message.parsed.characters:
            for char in response.choices[0].message.parsed.characters:
                character = self.retriever.retrieve_main_character_data(
                    self.context, char.characterId
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
            self.existing_characters, self.story_excerpt
        )
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(
            assist_content, sys_content, EnteringCharacterResponse
        )
        if not response.choices[0].message.parsed:
            raise StoryContextExceptions.NothingToParseError
        if response.choices[0].message.parsed.existing_characters:
            for char in response.choices[0].message.parsed.existing_characters:
                character = self.retriever.retrieve_main_character_data(
                    self.context, char.characterId
                )
                if character:
                    self.updater.add_character_to_current_context(self.context, character)
        if response.choices[0].message.parsed.new_characters:
            for char in response.choices[0].message.parsed.new_characters:
                await self.create_new_character(char)

    async def create_new_character(self, char: CharacterNameAndId) -> None:
        log.info("------------------ CREATING NEW LIFE --------------------------")
        assist_content = StoryPrompts.new_character_prompt(self.story_excerpt, char)
        sys_content = StoryPrompts.sys_instruct()
        response = await self.ai_query.query_gpt_general(assist_content, sys_content, Character)
        if response.choices[0].message.parsed:
            new_character = Character(**response.choices[0].message.parsed)
            self.updater.add_new_character_to_context(self.context, new_character)
