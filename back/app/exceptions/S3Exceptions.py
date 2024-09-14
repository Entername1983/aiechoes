from app.exceptions.exceptions import MyBaseError


class S3Exceptions:
    class NoResponseError(MyBaseError):
        def __init__(self, message: str = "No response from S3."):
            super().__init__(message)

    class NoBucketError(MyBaseError):
        def __init__(self, message: str = "No bucket found."):
            super().__init__(message)

    class NoObjectError(MyBaseError):
        def __init__(self, message: str = "No object found."):
            super().__init__(message)
