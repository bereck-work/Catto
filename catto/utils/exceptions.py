class PathNotFound(Exception):
    """
    This exception is raised when a path is not found.
    """

    pass


class InvalidImage(Exception):
    """
    This exception is raised when the URL provided is not an image.
    """

    pass


class AnimalFactNotFound(Exception):
    """
    This exception is raised when an animal fact related to the specific animal is not provided.
    """

    pass
