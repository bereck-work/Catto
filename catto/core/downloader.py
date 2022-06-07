import secrets
import sys
import time
from io import BytesIO
from pathlib import Path
from typing import Optional

import loguru
import requests
from PIL import Image
from PIL.Image import Image as PILImage
from typing import Dict
from rich.progress import track

from ..utils.enums import AnimalAPIEndpointEnum, AnimalResponseEnum
from ..utils.exceptions import InvalidImage, PathNotFound, AnimalFactNotFound
from ..utils.helpers import ExponentialBackoff

__all__ = ("Client",)


class Client:
    """
    A class that handles the requesting, parsing and downloading of images from the API endpoints specified in the enum
    :class:`AnimalAPIEndpoint`.
    """

    def __init__(self):
        self.logger = loguru.logger
        self.version = "1.0.5"
        self.__backoff = ExponentialBackoff(base=0.05, maximum_tries=5)
        self.session = requests.Session()
        self.__inner_url: Optional[str] = None

    def fetch_image_url_of_endpoint(self, animal: AnimalAPIEndpointEnum) -> Optional[str]:
        """
        This method fetches and returns the image url from the API for the specified animal category.

        Parameters:
            animal (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            Optional[str]: The url of the image.
        """

        response = self.session.get(AnimalAPIEndpointEnum[animal.name].value)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching image url for animal {animal.name} from  the API endpoint "
                f"{AnimalAPIEndpointEnum[animal.name].value}, "
                f"status code: {response.status_code}. Reason: {response.reason}"
            )
            return

        data: Dict[str, str] = response.json()
        enum_data = AnimalResponseEnum[animal.name]
        # This is a nifty way to get the image url from the json response. All I am doing is that I have an Enum
        # of the keys in the json response for each url for each animal category, and I am getting the value of
        # Enum, which basically stores the key, for example, https://some-random-api.ml/animal/cat, If you make a GET
        # request to the API, the API returns a json response, the image url is stored in the key named as 'image' and
        # KeyResponseImage.cats.value returns 'image' and then I index the json response with that key.
        # For example, if I have a json response like this:
        # {
        #     "image": "https://some-random-api.ml/animal/cat/image.jpg",
        #     "fact": "https://some-random-api.ml/animal/cat/fact.txt"
        # }
        # Then I can get the image url by doing:
        # data[AnimalResponseEnum.cats.value.key_that_contains_image]
        # This is a lazy way to get the image url from the json response, this is useful incase the API response
        # changes.
        # This is just a way to avoid unnecessary if-else statements.
        url_of_image: str = data[
            enum_data.value.key_that_contains_image_url
        ]  # Getting the corresponding url for the animal type using
        # the Enum which stores the key.
        return url_of_image

    def fetch_fact_about_the_animal(self, animal: AnimalAPIEndpointEnum) -> Optional[str]:
        """
        This method gets a random factual information about the specified animal category from
        the enum :class:`AnimalAPIEndpoint`.

        Parameters:
            animal (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            Optional[str]: The fact about the animal, if the API endpoint returns the fact in their json response, else
            None.
        """
        response = self.session.get(AnimalAPIEndpointEnum[animal.name].value)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching fact from API endpoint"
                f"{AnimalAPIEndpointEnum[animal.name].value}, "
                f"status code: {response.status_code}. Reason: {response.reason}"
            )
            return
        data: dict = response.json()
        enum_data = AnimalResponseEnum[animal.name]
        try:
            fact: str = data[enum_data.value.key_that_contains_fact]
        except KeyError:
            raise AnimalFactNotFound(
                f"The API endpoint didn't return any facts about '{animal.name}' in its json response."
            )
        return fact

    def save_image_from_url(self, url_of_image: str, path: Path) -> None:
        """
        This method takes an image url, fetches it, and saves it to the specified path.

        Parameters:
            url_of_image (str): This parameter takes the url of the image to download.
            path (pathlib.Path): This parameter takes the path to the directory where the image needs to be saved.

        Raises:
            PathNotFound: If the directory does not exist.
            InvalidImage: If the image is not a valid image.
        """
        if not path.is_dir():
            raise PathNotFound(f"{path.name} is not a valid directory.")
        response = self.session.get(url_of_image)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching the image from the image url: {url_of_image}, "
                f"status code: {response.status_code}. Reason: {response.reason}"
            )
            return

        data: bytes = response.content
        try:
            image: PILImage = Image.open(BytesIO(data))
        except Exception as e:
            raise InvalidImage(f"Exception occurred while opening image: {e}")

        image.save(
            f"{str(path.absolute())}/image-{secrets.token_hex(4)}.{image.format.lower()}",
            format=image.format.lower(),
        )
        return

    def download(self, animal: AnimalAPIEndpointEnum, amount: int, path: Path) -> None:
        """
        This method downloads the image from the url and saves it to the path.

        Parameters:
            animal (AnimalAPIEndpointEnum): This paramter takes the category of animal to download.
            path (pathlib.Path): This parameter takes the path to the directory to download the images into.
            amount (int): This paramter takes the amount of images to download.
        """
        try:
            ImageEnum = AnimalAPIEndpointEnum[animal.name]  # returns the enum for that
            # animal

        except KeyError:
            self.logger.error(
                f"Invalid animal selected: {animal.name}, please choose from: "
                f"{', '.join([animal.name for animal in AnimalAPIEndpointEnum])}"
            )
            sys.exit(1)
        for i in range(amount):
            data = self.fetch_image_url_of_endpoint(animal=ImageEnum)
            self.__inner_url = data
            try:
                self.save_image_from_url(url_of_image=data, path=path)

            except InvalidImage:
                self.logger.error(f"Image failed to load due to invalid image url: {self.__inner_url}, skipping image.")
                continue

            except PathNotFound:
                self.logger.error(f"Failed to save image to {path.name}.")
                sys.exit(1)

            for _ in track(
                range(amount),
                description=f"[bold][magenta]{i + 1}.) Downloading image: [bold][green]{self.__inner_url}",
            ):
                time.sleep(self.__backoff.calculate())  # This is a simple ratelimit handler to avoid
                # being banned from the API.
        return
