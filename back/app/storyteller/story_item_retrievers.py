from app.exceptions.StoryContextExceptions import StoryContextExceptions
from app.storyteller.storyteller_schemas import (
    Character,
    CharacterNameAndId,
    CurrentContext,
    Narrator,
    PlotPoint,
    Rules,
    StoryContext,
)


class StoryItemRetrievers:
    @staticmethod
    def retrieve_list_of_all_characters_in_story(context: StoryContext) -> list[CharacterNameAndId]:
        characters_list = []
        if context.characters and context.characters.mainCharacters:
            for character in context.characters.mainCharacters:
                name_and_id = {"characterId": character.id, "name": character.firstName}
                char_to_append = CharacterNameAndId(**name_and_id)
                characters_list.append(char_to_append)
        if context.characters and context.characters.secondaryCharacters:
            for character in context.characters.secondaryCharacters:
                name_and_id = {"characterId": character.id, "name": character.firstName}
                char_to_append = CharacterNameAndId(**name_and_id)
                characters_list.append(char_to_append)
        return characters_list

    @staticmethod
    def retrieve_main_character_data(context: StoryContext, character_id: str) -> Character | None:
        if context.characters:
            return next(
                (char for char in context.characters.mainCharacters if char.id == character_id),
                None,
            )
        return None

    @staticmethod
    def retrieve_secondary_character_data(
        context: StoryContext, character_id: str
    ) -> Character | None:
        if context.characters:
            return next(
                (
                    char
                    for char in context.characters.secondaryCharacters
                    if char.id == character_id
                ),
                None,
            )
        return None

    @staticmethod
    def retrieve_main_plot_point_data(context: StoryContext, plot_id: str) -> PlotPoint | None:
        if context.mainPlots:
            return next((plot for plot in context.mainPlots if plot.id == plot_id), None)
        return None

    @staticmethod
    def retrieve_secondary_plot_point_data(context: StoryContext, plot_id: str) -> PlotPoint | None:
        if context.subPlots:
            return next((plot for plot in context.subPlots if plot.id == plot_id), None)
        return None

    @staticmethod
    def retrieve_rules(context: StoryContext) -> Rules | None:
        if context.rules:
            return context.rules
        return None

    @staticmethod
    def retrieve_themes(context: StoryContext) -> list[str]:
        if context.themes:
            return context.themes
        return []

    @staticmethod
    def retrieve_narrator_data(context: StoryContext, narrator_id: str) -> Narrator | None:
        if context.narration and context.narration.narrators:
            return next(
                (
                    narrator
                    for narrator in context.narration.narrators
                    if narrator.id == narrator_id
                ),
                None,
            )
        return None

    @staticmethod
    def retrieve_current_context(context: StoryContext) -> CurrentContext | None:
        if context.currentContext:
            return context.currentContext
        return None


class StoryItemUpdater:
    @staticmethod
    def remove_character_from_current_context(
        context: StoryContext, character_id: str
    ) -> CurrentContext | None:
        if not context.currentContext:
            raise StoryContextExceptions.NoCurrentContextError
        if context.currentContext.charactersPresent:
            context.currentContext.charactersPresent = [
                character
                for character in context.currentContext.charactersPresent
                if character.characterId != character_id
            ]
        return context.currentContext

    @staticmethod
    def add_character_to_current_context(
        context: StoryContext, character: Character
    ) -> CurrentContext:
        if not context.currentContext:
            raise StoryContextExceptions.NoCurrentContextError
        name_and_id = {"characterId": character.id, "name": character.firstName}
        char_to_append = CharacterNameAndId(**name_and_id)
        if context.currentContext and context.currentContext.charactersPresent:
            context.currentContext.charactersPresent.append(char_to_append)
        return context.currentContext

    @staticmethod
    def add_new_character_to_context(
        context: StoryContext, character: Character, main_or_secondary: str = "main"
    ) -> StoryContext:
        if not context.characters:
            raise StoryContextExceptions.NoCharactersInContextError
        if main_or_secondary == "main":
            context.characters.mainCharacters.append(character)
        else:
            context.characters.secondaryCharacters.append(character)
        return context

    @staticmethod
    def update_existing_character_in_context(
        context: StoryContext, character: Character
    ) -> StoryContext:
        if not context.characters:
            raise StoryContextExceptions.NoCharactersInContextError
        if character in context.characters.mainCharacters:
            context.characters.mainCharacters.remove(character)
            context.characters.mainCharacters.append(character)
        else:
            context.characters.secondaryCharacters.remove(character)
            context.characters.secondaryCharacters.append(character)
        return context
