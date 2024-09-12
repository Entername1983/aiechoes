class MyBaseError(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, message: str = "An error has occurred."):
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
