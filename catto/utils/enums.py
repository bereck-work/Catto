from enum import Enum

__all__ = (
    "AnimalAPIEndpointEnum",
    "KeyResponseImageEnum",
    "KeyResponseFactEnum",
)


class EnumWithNoAliasing(Enum):
    """
    This class subclasses the :class:`Enum` class and overrides the __getattribute__ method to avoid
    the deduplication check. This is a workaround for labels that get aliased if the values are the same.
    Taken from https://stackoverflow.com/a/58273746 pretty cool.
    """

    def __init_subclass__(cls, *kargs, **kwargs):
        import inspect

        # unfortunately, there's no cleaner ways to retrieve original members
        for stack in reversed(inspect.stack()):
            frame_locals = stack[0].f_locals
            enum_members = frame_locals.get("enum_members")
            if enum_members is None:
                try:
                    enum_members = frame_locals["classdict"]._member_names
                except (KeyError, AttributeError):
                    continue
            break
        else:
            raise RuntimeError("Unable to checkout EnumWithNoAliasing members!")

        # patch subclass __getattribute__ to evade deduplication checks
        cls._shield_members = list(enum_members)
        cls._shield_getattr = cls.__getattribute__

        def patch(self, key):
            if key.startswith("_shield_"):
                return object.__getattribute__(self, key)
            if key.startswith("_value"):
                if not hasattr(self, "_name_"):
                    self._shield_counter = 0
                elif self._shield_counter < self._shield_members.index(self._name_):
                    self._shield_counter += 1

                    class unequal:
                        pass

                    return unequal
            return self._shield_getattr(key)

        cls.__getattribute__ = patch


class AnimalAPIEndpointEnum(EnumWithNoAliasing):
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
    racoon = "https://some-random-api.ml/animal/racoon"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class KeyResponseImageEnum(EnumWithNoAliasing):
    """
    This :class:`Enum` stores the API response keys which contain the image url for the specified animal API endpoint,
    as reffered in the :class:`AnimalAPIEndpoint` Enum.
    This enum basically maps the keys in the JSON response that contains the image URL for each animal API endpoint.
    """

    # There would be a better way to do this, but this way if the API response changes, I can just change the enum
    # value for the specific endpoint.
    dogs = "image"
    cats = "image"
    birds = "image"
    foxes = "image"
    pandas = "image"
    redpandas = "image"
    kangaroo = "image"
    racoon = "image"
    koala = "image"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class KeyResponseFactEnum(EnumWithNoAliasing):
    """
    This :class:`Enum` stores the API response keys which contain the `fact` for the specified animal API endpoint.
    This enum basically maps the keys in the JSON response that contains the `fact` for each animal API endpoint.
    """

    dogs = "fact"
    cats = "fact"
    birds = "fact"
    foxes = "fact"
    pandas = "fact"
    redpandas = "fact"
    kangaroo = "fact"
    racoon = "fact"
    koala = "fact"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
