# -*- coding: utf-8 -*-
from __future__ import annotations

import secrets
import sys
import time
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image
from PIL.Image import Image as PILImage  # weird naming
from loguru import logger
from rich.progress import track

from ..utils.enums import CategoryEnum, ResponseEnum
from ..utils.exceptions import (
    InvalidImageURL,
    PathNotFound,
    CategoryFactNotFound,
    ImageDownloadFailed,
    DataFetchFailed,
)
from ..utils.helpers import ExponentialBackoff

__all__ = ("Client",)


class Client:
    """
    A class that handles the requesting, parsing and downloading of images from the API endpoints specified in the enum
    :class:`AnimalAPIEndpoint`.
    """

    def __init__(self):
        self.__backoff = ExponentialBackoff(base=0.05)
        self.__inner_url: str | None = None

    @staticmethod
    def fetch_image_url_of_endpoint(animal: CategoryEnum) -> str | None:
        """
        This method fetches and returns the image url from the API response for the specified animal category.

        Parameters:
            animal (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            (str): The url of the image.
        """

        with httpx.Client(timeout=30) as client:
            response = client.get(url=str(CategoryEnum[animal.name].value))
        if response.status_code != 200:
            raise DataFetchFailed(
                f"Failed to fetch the image url for animal {animal.name} from  the API endpoint "
                f"{CategoryEnum[animal.name].value}.",
                status_code=response.status_code,
                reason=response.reason_phrase,
                url=response.url.__str__(),
            )

        data: dict[str, str] = response.json()
        enum_data = ResponseEnum[animal.name]
        # This is a nifty way to get the image url from the json response. All I am doing is that I have an Enum of
        # the keys in the json response for each url for each animal category, and I am getting the value of Enum,
        # which basically stores the key, for example, https://some-random-api.ml/animal/cat. If I make a GET HTTP
        # request to the API endpoint, I get a json response such as:
        # {
        # "fact": "A random fact about cats",
        # "image": "some_image_url"
        # }
        # There are two keys in the json response, one for the fact and one for the
        # image. The json response for the specified endpoint is mapped in a dataclass called as ResponseInterface,
        # Each of the endpoint's json responses are mapped in the class ResponseInterface, which is stored in an Enum
        # called ResponseEnum. So whenever I index the enum using a specific animal category, I get a dataclass
        # that contains the keys for the fact and image, and I can get the value of the key that I need.
        # For e.g.
        # ResponseEnum.cats.value.key_that_contains_fact will return "fact" which is the key that contains the
        # fact about cats in the json response.
        # This is just a way to avoid unnecessary if-else statements.
        url_of_image: str = data[
            enum_data.interface.key_that_contains_image_url
        ]  # Getting the corresponding url for the animal type using
        # the Enum which stores the key.
        return url_of_image

    @staticmethod
    def fetch_fact_about_the_category(category: CategoryEnum) -> str | None:
        """
        This method gets a random factual information about the specified animal category from
        the enum :class:`AnimalAPIEndpoint`.

        Parameters:
            category (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            Optional[str]: The fact about the animal, if the API endpoint returns the fact in their json response, else
            None.
        """
        with httpx.Client(timeout=30.0) as client:
            response = client.get(str(CategoryEnum[category.name].value))

        if response.status_code != 200:
            logger.error(
                f"Error occurred while fetching fact from API endpoint"
                f"{CategoryEnum[category.name].value}\n"
                f"Status code: {response.status_code}\nReason: {response.reason_phrase}"
            )
            return
        data: dict[str, str] = response.json()
        enum_data = ResponseEnum[category.name]
        try:
            fact: str = data[enum_data.interface.key_that_contains_fact]
        except KeyError:
            raise CategoryFactNotFound(
                f"The API endpoint didn't return any facts about '{category.name}' in its json response."
            )
        return fact

    @staticmethod
    def save_image_from_url(
        url_of_image: str, path: Path, animal: CategoryEnum
    ) -> dict[str, str | Path] | None:
        """
        This method takes an image url, fetches it, and saves it to the specified path.

        Parameters:
            url_of_image (str): This parameter takes the url of the image to download.
            path (pathlib.Path): This parameter takes the path to the directory where the image needs to be saved.
            animal (CategoryEnum): This parameter takes the animal category that the user chose.

        Returns:
           Optional[dict[str, Union[str, Path, Image]]]: A dictionary containing the path to directory, where the images are
                                                 saved, the name of the image file and the image as a :class:`PIL.Image`
                                                 object.

        Raises:
            PathNotFound: If the directory does not exist.
            InvalidImage: If the image is not a valid image.
        """
        if not path.is_dir():
            raise PathNotFound(f"'{path.name}' is not a valid directory.")

        with httpx.Client(timeout=30.0) as client:
            response = client.get(url_of_image, follow_redirects=True)

        if response.status_code != 200:
            raise DataFetchFailed(
                f"Failed to fetch image from url '{url_of_image}",
                status_code=response.status_code,
                reason=response.reason_phrase,
                url=url_of_image,
            )

        data: bytes = response.content
        try:
            image: PILImage = Image.open(BytesIO(data))
        except Exception as e:
            raise InvalidImageURL(
                f"Failed to read image from url {response.url}.\nReason: {e}"
            )
        hex_code = secrets.token_hex(4)

        try:
            image.save(
                f"{str(path.absolute())}/{animal.name}-image-{hex_code}.{image.format.lower()}",
                format=image.format.lower(),
            )
        except Exception as e:
            raise ImageDownloadFailed(
                f"An exception occurred while trying to save an image: {image.info}/n{e}",
                image=image.info,
                reason=str(e),
            )

        return {
            "path": path.absolute(),
            "name": f"{animal.name}-image-{hex_code}.{image.format.lower()}",
        }

    def download(
        self, animal: CategoryEnum, amount: int, path: Path
    ) -> dict[str, Path | list[str]]:
        """
        This method downloads the image from the url and saves it to the path.

        Parameters:
            animal (CategoryEnum): This parameter takes the category of animal to download.
            path (pathlib.Path): This parameter takes the path to the directory to download the images into.
            amount (int): This parameter takes the amount of images to download.

        Returns:
            dict[str, Union[list[str], Path]]: A dictionary containing the names of the images that were downloaded,
                                               and the directory as a Path object.
        """
        image_names: list[str] = []
        try:
            ImageEnum = CategoryEnum[animal.name]  # returns the enum for that
            # animal

        except KeyError:
            logger.error(
                f"Invalid animal selected: {animal.name}, please choose from: "
                f"{', '.join([animal.name for animal in CategoryEnum])}"
            )
            sys.exit(1)
        for i in range(amount):
            try:
                url = self.fetch_image_url_of_endpoint(animal=ImageEnum)
            except DataFetchFailed as e:
                logger.error(
                    f"Error occurred while fetching image url for animal {animal.name} from  the API endpoint "
                    f"{CategoryEnum[animal.name].value}.\n"
                    f"Status code: {e.status_code}.\nReason: {e.reason}"
                )
                continue
            self.__inner_url = url
            try:
                data = self.save_image_from_url(
                    url_of_image=url, path=path, animal=ImageEnum
                )
                image_names.append(data["name"])

            except InvalidImageURL:
                logger.warning(
                    f"Image failed to load due to invalid image url: {self.__inner_url}, skipping.."
                )
                continue

            except DataFetchFailed as e:
                logger.error(
                    f"Error occurred while fetching the image from the image url: {e.url}\n"
                    f"Status code: {e.status_code}.\nReason: {e.reason}"
                )
                sys.exit(1)

            except ImageDownloadFailed as e:
                logger.error(
                    f"Error occurred while trying to save the image {e.image}\nReason: {e.reason}"
                )
                continue

            except PathNotFound:
                logger.error(
                    f"Directory '{path.name}' does not exist in parent directory '{path.absolute().parent.name}', "
                    f"failed to save image."
                )
                sys.exit(1)

            for _ in track(
                range(amount),
                description=f"[bold][magenta]{i + 1}.) Saving image [bold][green]{data['name']}: "
                f"[bold][blue with underline]"
                f"{self.__inner_url}",
            ):
                time.sleep(
                    self.__backoff.calculate()
                )  # This is a simple ratelimit handler to avoid
                # being banned from the API.
        return {"names": image_names, "directory": path.absolute()}
