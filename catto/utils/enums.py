from dataclasses import dataclass
from enum import Enum

__all__ = ("AnimalAPIEndpointEnum", "AnimalResponseEnum", "ColorEnum")

from typing import Optional


class AnimalAPIEndpointEnum(Enum):
    """
    This :class:`Enum` stores animal API enpoint urls based on the animal category.
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

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class ResponseInterface:
    """
    This :class:`dataclass` stores the keys in the json response for each animal category. This is mainly used to
    get the image url and the fact from the json response.
    """

    endpoint: AnimalAPIEndpointEnum
    key_that_contains_image_url: Optional[str] = None
    key_that_contains_fact: Optional[str] = None


class AnimalResponseEnum(Enum):
    """
    This :class:`Enum` stores the API response keys in :class:`ResponseInterface` which contain the image url and the fact
    for the specified animal API endpoint, as reffered in the :class:`AnimalAPIEndpoint` Enum.
    This enum basically maps the keys in the JSON response that contains the image URL for each animal API endpoint.
    """

    # There would be a better way to do this, but this way if the API response changes, I can just change the enum
    # value for the specific endpoint.
    dogs = ResponseInterface(AnimalAPIEndpointEnum.dogs, "image", "fact")
    cats = ResponseInterface(AnimalAPIEndpointEnum.cats, "image", "fact")
    birds = ResponseInterface(AnimalAPIEndpointEnum.birds, "image", "fact")
    foxes = ResponseInterface(AnimalAPIEndpointEnum.foxes, "image", "fact")
    pandas = ResponseInterface(AnimalAPIEndpointEnum.pandas, "image", "fact")
    redpandas = ResponseInterface(AnimalAPIEndpointEnum.redpandas, "image", "fact")
    kangaroo = ResponseInterface(AnimalAPIEndpointEnum.kangaroo, "image", "fact")
    raccoon = ResponseInterface(AnimalAPIEndpointEnum.raccoon, "image", "fact")
    koala = ResponseInterface(AnimalAPIEndpointEnum.koala, "image", "fact")

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class ColorEnum(Enum):
    """
    This class subclasses the :class:`Enum` class and stores the color names.
    """

    black = "black"
    red = "red"
    green = "green"
    yellow = "yellow"
    blue = "blue"
    magenta = "magenta"
    cyan = "cyan"
    white = "white"
    gray = "gray"
    grey = "gray"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
