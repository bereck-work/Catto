from enum import Enum


class ImageType(Enum):
    """
    Enum for animal Image types.
    """

    dogs = "https://dog.ceo/api/breeds/image/random"
    cats = "https://aws.random.cat/meow"
    birds = "https://random.birb.pw/tweet/image"
    foxes = "https://randomfox.ca/floof/"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class KeyResponse(Enum):
    """
    Enum for keys in the JSON response.
    """

    dogs = "message"
    cats = "file"
    birds = "url"
    foxes = "image"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
