# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


__all__ = ("CategoryEnum", "ResponseEnum", "ColorEnum")


class CategoryEnum(Enum):
    """
    This :class:`Enum` stores animal API endpoint urls based on the animal category.
    """

    pandas = "https://some-random-api.ml/animal/panda"
    dogs = "https://some-random-api.ml/animal/dog"
    cats = "https://some-random-api.ml/animal/cat"
    birds = "https://some-random-api.ml/animal/birb"
    foxes = "https://some-random-api.ml/animal/fox"
    redpandas = "https://some-random-api.ml/animal/red_panda"
    kangaroo = "https://some-random-api.ml/animal/kangaroo"
    koala = "https://some-random-api.ml/animal/koala"
    raccoon = "https://some-random-api.ml/animal/raccoon"

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class ResponseInterface:
    """
    This :func:`dataclass` stores the keys in the json response for each animal category. This is mainly used to
    get the image url and the fact from the json response.
    """

    endpoint: CategoryEnum
    key_that_contains_image_url: str | None = None
    """
    The key that contains the url of the image to be indexed in the json data.
    """
    key_that_contains_fact: str | None = None
    """
    The key that contains factual information about the animal category to be indexed in the json data.
    """


class ResponseEnum(Enum):
    """
    This :class:`Enum` stores the API response keys stored as :class:`ResponseInterface` which contains
    the image url and the fact for the specified animal API endpoint, as referred in the :class:`AnimalAPIEndpoint`
    Enum.This enum basically maps the keys in the JSON response that contains the image URL for each animal API
    endpoint.
    """

    # There would be a better way to do this, but this way if the API response changes, I can just change the enum
    # value for the specific endpoint.
    dogs = ResponseInterface(CategoryEnum.dogs, "image", "fact")
    cats = ResponseInterface(CategoryEnum.cats, "image", "fact")
    birds = ResponseInterface(CategoryEnum.birds, "image", "fact")
    foxes = ResponseInterface(CategoryEnum.foxes, "image", "fact")
    pandas = ResponseInterface(CategoryEnum.pandas, "image", "fact")
    redpandas = ResponseInterface(CategoryEnum.redpandas, "image", "fact")
    kangaroo = ResponseInterface(CategoryEnum.kangaroo, "image", "fact")
    raccoon = ResponseInterface(CategoryEnum.raccoon, "image", "fact")
    koala = ResponseInterface(CategoryEnum.koala, "image", "fact")

    @property
    def interface(self) -> ResponseInterface:
        """
        This property returns the value of a AnimalResponseEnum label as a :class:`ResponseInterface` object.
        """
        return self.value  # noqa

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class ColorEnum(Enum):
    """
    This class subclasses the :class:`Enum` class and stores the color names.
    """

    black = "black", "underline"
    brown = "brown", "underline"
    red = "red", "underline"
    green = "green", "underline"
    yellow = "yellow", "underline"
    blue = "blue", "underline"
    magenta = "magenta", "underline"
    violet = "violet", "underline"
    cyan = "cyan", "underline"
    white = "white", "underline"
    gray = "gray", "underline"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, underline: str = None):
        self._underline_ = underline

    # this makes sure that the description is read-only
    @property
    def underline(self) -> str:
        """
        This property returns the ColorEnum with 'underline'.

        For example: ColorEnum.blue.underline >> blue underline
        """
        return f"{self.value} {self._underline_}"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
