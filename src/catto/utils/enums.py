from enum import Enum


class ImageType(Enum):
    """
    This :class:`Enum` stores animal API enpoint urls based on the animal category.
    """

    panda = "https://some-random-api.ml/animal/panda"
    dogs = "https://some-random-api.ml/animal/dog"
    cats = "https://some-random-api.ml/animal/cat"
    birds = "https://some-random-api.ml/animal/birb"
    foxes = "https://some-random-api.ml/animal/fox"
    red_panda = "https://some-random-api.ml/animal/red_panda"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class KeyResponseImage(Enum):
    """
    This :class:`Enum` stores the API response keys which contain the image url for the specified animal API endpoint.
    This enum basically maps the keys in the JSON response that contains the image URL for each animal API endpoint.
    """

    # There would be a better way to do this, but this way if the API response changes, I can just change the enum
    # value for the specific endpoint.
    dogs = "image"
    cats = "image"
    birds = "image"
    foxes = "image"
    panda = "image"
    red_panda = "image"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class KeyResponseFact(Enum):
    """
    This :class:`Enum` stores the API response keys which contain the `fact` for the specified animal API endpoint.
    This enum basically maps the keys in the JSON response that contains the `fact` for each animal API endpoint.
    """

    dogs = "fact"
    cats = "fact"
    birds = "fact"
    foxes = "fact"
    panda = "fact"
    red_panda = "fact"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
