from app.exceptions.exceptions import MyBaseError


class StoryContextExceptions:
    class CharacterNotFoundError(MyBaseError):
        def __init__(self, message: str = "Did not find character in story context."):
            super().__init__(message)
