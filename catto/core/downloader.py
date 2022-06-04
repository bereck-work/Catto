import secrets
import sys
import time
import typing
from io import BytesIO
from pathlib import Path
from typing import Optional
from rich.progress import track
import loguru
import requests
from PIL import Image
from PIL.Image import Image as PILImage

from ..utils.enums import AnimalAPIEndpointEnum, KeyResponseFactEnum, KeyResponseImageEnum
from ..utils.exceptions import InvalidImage, PathNotFound, AnimalFactNotFound
from ..utils.helpers import ExponentialBackoff

__all__ = ("Client",)


class Client:
    """
    A class that handles the downloading of images from the API endpoints specified in the enum
    :class:`AnimalAPIEndpoint`.
    """

    def __init__(self):
        self.logger = loguru.logger
        self.version = "1.0.3`"
        self.__backoff = ExponentialBackoff(base=0.05, maximum_tries=5)
        self.session = requests.Session()
        self.animal_category_dict = {
            animal.name: animal for animal in AnimalAPIEndpointEnum
        }  # This is a dictionary that stores the animal category and the corresponding API endpoint.

        self.json_response_key_containing_image_url_dict = {
            response.name: response for response in KeyResponseImageEnum
        }  # This is a dictionary that stores the animal category and the corresponding key in the json response, that
        # contains the image url.

        self.json_response_key_containing_fact_dict = {
            fact_response.name: fact_response for fact_response in KeyResponseFactEnum
        }  # This is a dictionary that stores the animal category and the corresponding key in the json response, that
        # contains the fact.
        self.__inner_url: Optional[str] = None

    def get_image_url_of_the_animal(self, url: str, animal: AnimalAPIEndpointEnum) -> Optional[str]:
        """
        This method fetches and returns the image url from the API for the specified animal category.

        Parameters:
            url (str): This parameter takes the url of the API endpoint.
            animal (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            Optional[str]: The url of the image.
        """

        response = self.session.get(url)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching image url for animal {animal.name} from  the API endpoint "
                f"{self.animal_category_dict[animal.name].value}, "
                f"status code: {response.status_code}. This error can occur if the API is down, "
                f"you are not connected to internet or the API is not working properly."
            )
            return
        if response.status_code == 429:
            self.logger.warning(
                f"The API endpoint {self.animal_category_dict[animal.name].value} has been rate limited. "
                f"Please 'catto status' to check the status of the API."
            )

        data: dict = response.json()
        key_in_which_image_url_is_stored: typing.Optional[
            KeyResponseImageEnum
        ] = self.json_response_key_containing_image_url_dict[animal.name]
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
        # data[KeyResponseImage.cats.value]
        # This is a lazy way to get the image url from the json response, incase the API changes.
        # This is just a way to avoid unnecessary if-else statements.
        url_of_image: str = data[
            key_in_which_image_url_is_stored.value
        ]  # Getting the corresponding url for the animal type using
        # the Enum which stores the key.
        return url_of_image

    def get_fact_about_the_animal(self, animal: AnimalAPIEndpointEnum) -> Optional[str]:
        """
        This method gets a random factual information about the specified animal category from
        the enum :class:`AnimalAPIEndpoint`.

        Parameters:
            animal (AnimalAPIEndpoint): This parameter takes the animal category from the enum.

        Returns:
            Optional[str]: The fact about the animal, if the API endpoint returns the fact in their json response, else
            None.
        """
        response = self.session.get(self.animal_category_dict[animal.name].value)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching fact from API endpoint"
                f"{self.animal_category_dict.get(animal.name).value}, "
                f"status code: {response.status_code}. This error can occur if the API is down, you are not connected "
                f"to the internet or the API is not working properly."
            )
            return
        data: dict = response.json()
        key_in_which_fact_is_stored: KeyResponseFactEnum = self.json_response_key_containing_fact_dict[animal.name]
        try:
            fact: str = data[key_in_which_fact_is_stored.value]
        except KeyError:
            raise AnimalFactNotFound(
                f"The API endpoint hasn't return the fact about {animal.name} in their json response."
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
                f"status code: {response.status_code}. This error can occur if the image url that was provided "
                f"is invalid."
            )
            return
        if response.status_code == 429:
            self.logger.warning(
                f"The API endpoint {self.animal_category_dict[AnimalAPIEndpointEnum.cats.name].value} has been rate "
                f"limited. Please 'catto status' to check the status of the API."
            )

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
            ImageEnum: AnimalAPIEndpointEnum = self.animal_category_dict[animal.name]  # returns the enum for that
            # animal

        except KeyError:
            self.logger.error(
                f"Invalid animal selected: {animal.name}, please choose from: "
                f"{', '.join(list(self.animal_category_dict.keys()))}"
            )
            sys.exit(1)
        for i in range(amount):
            data = self.get_image_url_of_the_animal(url=ImageEnum.value, animal=ImageEnum)
            self.__inner_url = data
            for j in track(
                range(amount), description=f"[bold][magenta]{i + 1}.) " f"Downloading image: {self.__inner_url}"
            ):
                try:
                    self.save_image_from_url(data, path)
                    time.sleep(self.__backoff.calculate())  # This is a simple ratelimit handler to avoid
                    # being banned from the API.

                except InvalidImage:
                    self.logger.error(
                        f"Image failed to load due to invalid image url: {self.__inner_url}, skipping image."
                    )
                    continue

                except PathNotFound:
                    self.logger.error(f"Failed to save image to {path.name}.")
                    sys.exit(1)
        return
