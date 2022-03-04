import pathlib
import random
import sys
from io import BytesIO
from typing import Optional

import loguru
import requests
from PIL import Image
from alive_progress import alive_bar
from colorama import Fore

from ..utils.exceptions import PathNotFound, InvalidImage
from ..utils.enums import ImageType, KeyResponse


class Client:
    """
    A class that handles the downloading of images from the API.
    """

    def __init__(self):
        self.logger = loguru.logger
        self.bold_color = "\033[1m"
        self.animal_category_dict = {
            "cats": ImageType.cats,
            "dogs": ImageType.dogs,
            "foxes": ImageType.foxes,
            "birds": ImageType.birds,
        }

        self.json_response_key_dict = {
            "cats": KeyResponse.cats,
            "dogs": KeyResponse.dogs,
            "foxes": KeyResponse.foxes,
            "birds": KeyResponse.birds,
        }
        self.__inner_url = None

    def get_image_from_url(self, url: str, animal: ImageType) -> Optional[str]:
        """
        This method gets a cat image from the API.

        Returns:
            Optional[str]: The url of the image.
        """

        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error(
                f"Error occurred while fetching image from {url}, status code: {response.status_code}"
            )
            return
        data: dict = response.json()
        key = self.json_response_key_dict.get(animal.name)
        # This is a nifty way to get the image url from the json response. All I am doing is that I have an Enum
        # of the keys in the json response for each url for each animal category, and I am getting the value of
        # Enum, which basically stores the key, for example, https://aws.random.cat/meow If you make a GET
        # request to the url, you will get a json response, the image url is a key named as 'file' and
        # KeyResponse.cats.value returns 'file' and then I get the image url for the cute cat image. Just wanted
        # to avoid if statements.
        url_of_image = data.get(
            key.value
        )  # Getting the corresponding url for the animal type using
        # the Enum which stores the key.
        return url_of_image

    @staticmethod
    def save_image_from_url(url_of_image: str, path: str):
        """
        This method takes an image url, fetches it, and saves it to the specified path.

        Parameters
        ----------
        url_of_image : str
            The image to be saved in BytesIO format.
        path : str
            The path to save the image to.
        """
        path = pathlib.Path(path)
        if not path.is_dir():
            raise PathNotFound(f"{path} is not a directory.")
        response = requests.get(url_of_image)
        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            raise InvalidImage(f"Exception occurred while opening image: {e}")
        image.save(
            f"{path}/image{random.randrange(1, 999)}.{image.format.lower()}",
            format=image.format.lower(),
        )

    def download(self, animal: str, amount: int, path: str):
        """
        This method downloads the image from the url and saves it to the path.

        Args:
            animal (str): The type of animal image to download.
            path (str): The path to download the images to.
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
            data = self.get_image_from_url(url=image_url.value, animal=image_url)
            self.__inner_url = data
            with alive_bar(
                1,
                force_tty=True,
                title=f"{self.bold_color}{Fore.LIGHTGREEN_EX}Downloading {i + 1}. {Fore.BLUE}{self.__inner_url}",
            ) as bar:
                try:
                    self.save_image_from_url(url_of_image=self.__inner_url, path=path)
                    bar()
                except InvalidImage:
                    self.logger.error(
                        f"Failed to load image from {self.__inner_url}, skipping..."
                    )
                    continue
                except PathNotFound:
                    self.logger.error(f"Failed to save image to {path}.")
                    sys.exit(1)
