class BaseError(Exception):
    """
    Base exception class for all Catto exceptions.
    """

    pass


class PathNotFound(BaseError):
    """
    Raised when a path is not found.
    """

    pass


class InvalidImage(BaseError):
    """
    Raised when the URL is not an image.
    """

    pass
