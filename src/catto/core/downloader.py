import random
import sys
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import loguru
import requests
from alive_progress import alive_bar
from colorama import Fore
from PIL import Image
from PIL.Image import Image as PILImage

from catto.utils.enums import ImageType, KeyResponseFact, KeyResponseImage
from catto.utils.exceptions import InvalidImage, PathNotFound


class Client:
    """
    A class that handles the downloading of images from the API.
    """

    def __init__(self):
        self.logger = loguru.logger
        self.bold_color = "\033[1m"
        self.session = requests.Session()
        self.animal_category_dict = {
            "cats": ImageType.cats,
            "dogs": ImageType.dogs,
            "foxes": ImageType.foxes,
            "birds": ImageType.birds,
            "panda": ImageType.panda,
            "red_panda": ImageType.red_panda,
        }

        self.json_response_key_containing_image_url_dict = {
            "cats": KeyResponseImage.cats,
            "dogs": KeyResponseImage.dogs,
            "foxes": KeyResponseImage.foxes,
            "birds": KeyResponseImage.birds,
            "panda": KeyResponseImage.panda,
            "red_panda": KeyResponseImage.red_panda,
        }
        self.json_response_key_containing_fact_dict = {
            "cats": KeyResponseFact.cats,
            "dogs": KeyResponseFact.dogs,
            "foxes": KeyResponseFact.foxes,
            "birds": KeyResponseFact.birds,
            "panda": KeyResponseFact.panda,
            "red_panda": KeyResponseFact.red_panda,
        }
        self.__inner_url: Optional[str] = None

    def get_image_url_of_the_animal(self, url: str, animal: ImageType) -> Union[str, None]:
        """
        This method fetches and returns the image url from the API for the specified animal category.

        Returns:
            Optional[str]: The url of the image.
        """

        response = self.session.get(url)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching image url from {url}, status code: {response.status_code}"
            )
            return None
        data: dict = response.json()
        key_in_which_image_url_is_stored = self.json_response_key_containing_image_url_dict.get(animal.name)
        # This is a nifty way to get the image url from the json response. All I am doing is that I have an Enum
        # of the keys in the json response for each url for each animal category, and I am getting the value of
        # Enum, which basically stores the key, for example, https://some-random-api.ml/animal/cat, If you make a GET
        # request to the API, the API returns a json response, the image url is stored in the key named as 'image' and
        # KeyResponseImage.cats.value returns 'image' and then I get the image url for the cute cat image.
        # This is just a way to avoid unnecessary if-else statements.
        url_of_image = data.get(
            key_in_which_image_url_is_stored.value
        )  # Getting the corresponding url for the animal type using
        # the Enum which stores the key.
        return url_of_image

    def get_fact_about_the_animal(self, animal: ImageType) -> Union[str, None]:
        """
        This method gets a random factual information about the animal.

        Returns:
            Optional[str]: The fact about the animal.
        """
        response = self.session.get(self.animal_category_dict.get(animal.name).value)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching a fact about {animal.name}, status code: {response.status_code}"
            )
            return None
        data: dict = response.json()
        key_in_which_fact_is_stored: KeyResponseFact = self.json_response_key_containing_fact_dict.get(animal.name)
        fact = data.get(key_in_which_fact_is_stored.value)
        return fact

    def save_image_from_url(self, url_of_image: str, directory: str):
        """
        This method takes an image url, fetches it, and saves it to the specified path.

        Args:
            url_of_image (str): The url of the image.
            directory (str): The directory where the image is to be saved.

        """
        path: Path = Path(directory)
        if not path.is_dir():
            raise PathNotFound(f"{path} is not a directory.")
        response = self.session.get(url_of_image)
        try:
            image: PILImage = Image.open(BytesIO(response.content))
        except Exception as e:
            raise InvalidImage(f"Exception occurred while opening image: {e}")
        image.save(
            f"{path}/image{random.randrange(1, 999)}.{image.format.lower()}",
            format=image.format.lower(),
        )

    def download(self, animal: str, amount: int, directory: str):
        """
        This method downloads the image from the url and saves it to the path.

        Args:
            animal (str): The type of animal image to download.
            directory (str): The path to download the images to.
            amount (int): The amount of images to download.
        """
        try:
            image_url = self.animal_category_dict[animal.lower()]
        except KeyError:
            self.logger.error(
                f"Invalid animal selected: {animal}, please choose from: "
                f"{', '.join(list(self.animal_category_dict.keys()))}"
            )
            sys.exit(1)

        for i in range(amount):
            data = self.get_image_url_of_the_animal(url=image_url.value, animal=image_url)
            self.__inner_url = data
            with alive_bar(
                1,
                force_tty=True,
                title=f"{self.bold_color}{Fore.LIGHTGREEN_EX}Downloading {i + 1}. {Fore.BLUE}{self.__inner_url}",
            ) as bar:
                try:
                    self.save_image_from_url(url_of_image=self.__inner_url, directory=directory)
                    bar()
                except InvalidImage:
                    self.logger.error(f"Failed to load image from {self.__inner_url}, skipping...")
                    continue
                except PathNotFound:
                    self.logger.error(f"Failed to save image to {directory}.")
                    sys.exit(1)
