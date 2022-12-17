# -*- coding: utf-8 -*-z

__all__ = (
    "PathNotFound",
    "InvalidImageURL",
    "CategoryFactNotFound",
    "DataFetchFailed",
    "ImageDownloadFailed",
)


class PathNotFound(Exception):
    """
    This exception is raised when a path is not found or does not exist.
    """

    pass


class InvalidImageURL(Exception):
    """
    This exception is raised when the URL provided is not an image.
    """

    pass


class CategoryFactNotFound(Exception):
    """
    This exception is raised when an animal fact related to the specific animal is not provided.
    """

    pass


class ImageDownloadFailed(Exception):
    """
    This exception is raised when an image has failed to download.
    """

    def __init__(self, error: str, /, image, reason: str):
        self.image = image
        self.reason = reason


class DataFetchFailed(Exception):
    """
    This exception is raised when the API request fails return the expected data.
    """

    def __init__(self, error: str, /, status_code: int, reason: str, url: str):
        self.status_code = status_code
        self.reason = reason
        self.url = url
