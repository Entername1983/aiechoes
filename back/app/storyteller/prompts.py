from app.storyteller.storyteller_schemas import CharacterNameAndId

prompts = {
    "initialize": "You are the first player in a game of exquisite corpse.  Write one sentence that other players will build on",
    "reply": "You are playing a game of exquisite corpse, you should continue the story based on the previous players sentence.  The previous player wrote: ",
}


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
    def entering_character_prompt(existing_characters: str, story_excerpt: str) -> str:
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
    def identify_character_changes(story_excerpt: str, char_list: str) -> str:
        return f"""Identify whether any of the following characters {char_list} underwent any
        changes in the following excerpt {story_excerpt}. Return whether characters have changed
        or not and Return a list of character Ids,
        their names and the changes according to the format provided"""

    @staticmethod
    def update_character_info(char_string: str, changes: str) -> str:
        return f"""Update the character details for the following character {char_string}
        with the changes {changes} and fill out the details according to the format provided"""

    @staticmethod
    def story_prompt_with_context(story_context: str, prev_replies_string: str) -> str:
        return f"""This is the current context of a story in progress:\n {story_context}\n
        You are tasked with writting the next sentence in a story. The previous 5 sentences
        written by players are:\n
        {prev_replies_string}.\n Please write the next sentence to continue the story.
        Only reply with the next sentence you would like to add to the story.
        Do not include any markdown or formatting or anything other than the
        sentence that continues the story. You must not reply with anything other than the next
        sentence."""

    @staticmethod
    def story_prompt_without_context(prev_replies_string: str) -> str:
        return f"""You are tasked with writting the next sentence in a story. The previous 5 sentences
        written by players are:\n
        {prev_replies_string}.\n Please write the next sentence to continue the story.
        Only reply with the next sentence you would like to add to the story.
        Do not include any markdown or formatting or anything other than the
        sentence that continues the story. You must not reply with anything other than the next
        sentence."""
