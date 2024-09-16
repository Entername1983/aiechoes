from app.exceptions.exceptions import MyBaseError


class CallAiExceptions:
    class NoResponseError(MyBaseError):
        def __init__(self, message: str = "No response from AI."):
            super().__init__(message)

    class InvalidResponseError(MyBaseError):
        def __init__(self, message: str = "Invalid response from AI."):
            super().__init__(message)

    class InvalidLlmError(MyBaseError):
        def __init__(self, message: str = "Invalid LLM."):
            super().__init__(message)

    class NoLlmSelectedError(MyBaseError):
        def __init__(self, message: str = "No LLM selected."):
            super().__init__(message)

    class NoPromptError(MyBaseError):
        def __init__(self, message: str = "No prompt."):
            super().__init__(message)

    class NoPreviousReplyError(MyBaseError):
        def __init__(self, message: str = "No previous reply."):
            super().__init__(message)

    class ResponseTooLongError(MyBaseError):
        def __init__(self, message: str = "Response too long."):
            super().__init__(message)

    class NoImageUrlError(MyBaseError):
        def __init__(self, message: str = "No image URL."):
            super().__init__(message)
