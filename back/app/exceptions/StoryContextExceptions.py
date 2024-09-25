from app.exceptions.exceptions import MyBaseError


class StoryContextExceptions:
    class CharacterNotFoundError(MyBaseError):
        def __init__(self, message: str = "Did not find character in story context."):
            super().__init__(message)

    class NoCurrentContextError(MyBaseError):
        def __init__(self, message: str = "No current context in story context."):
            super().__init__(message)

    class NoCharactersInContextError(MyBaseError):
        def __init__(self, message: str = "No characters in story context."):
            super().__init__(message)

    class NothingToParseError(MyBaseError):
        def __init__(self, message: str = "No parsed data from AI response."):
            super().__init__(message)
