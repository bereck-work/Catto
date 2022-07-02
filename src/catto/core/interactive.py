import getpass
import os
import pathlib
import sys
import time
from pathlib import Path
from typing import Optional
import loguru
import pyfiglet
import questionary
from colorama import Fore
from rich.console import Console
from ..core.downloader import Client
from ..utils import AnimalFactNotFound, AnimalAPIEndpointEnum, ColorEnum
from ..utils.helpers import interactive_print

__all__ = ("Controller",)


class Controller:
    """
    This class is responsible for the interactive mode of the program.
    """

    def __init__(self):
        self.client = Client()
        self.console = Console()
        self.logger = loguru.logger

    @staticmethod
    def print_logo(typewriter_effect: bool = False) -> None:
        """
        This method prints the logo of the application.
        """
        figlet_text = pyfiglet.figlet_format("Catto", font="slant")
        if typewriter_effect:
            for i in figlet_text:
                print(f"{Fore.YELLOW}{i}", end="", flush=True)
                time.sleep(0.03)
            return
        interactive_print(text=figlet_text, color=ColorEnum.yellow, bold=True)
        return

    def fetch_random_fact_about_the_selected_animal(self, animal: AnimalAPIEndpointEnum) -> Optional[str]:
        """
        This method returns a random fact about the animal that the user selected.

        Parameters:
            animal (AnimalAPIEndpointEnum): This parameter takes animal that the user selected.

        Returns:
            fact (Optional[str]): The fact about the animal.

        Raises:
            AnimalFactNotFound: If the API's json response does not contain a fact about the animal.
        """
        animal_type = AnimalAPIEndpointEnum[animal.name]
        fact = self.client.fetch_fact_about_the_animal(animal_type)
        if fact is None:
            raise AnimalFactNotFound()
        return fact

    @staticmethod
    def ask_for_animal_choice() -> AnimalAPIEndpointEnum:
        """
        This method asks the user for the amount of images to download.

        Returns:
            animal_choice (str): The animal that the user selected.
        """
        user_choice: str = questionary.select(
            "Select the category of animal to download: ", choices=[animal.name for animal in AnimalAPIEndpointEnum]
        ).ask()
        return AnimalAPIEndpointEnum[user_choice]

    def ask_for_amount_of_images(self) -> int:
        """
        This method asks the user for the amount of images that they want to download.

        Returns:
            amount_of_images (int): The amount of images to download.
        """
        user_choice = questionary.text(
            "The amount of images you want to download?",
            default="1",
        ).ask()
        if not user_choice.isdigit():
            interactive_print("Please provide a valid integer.", bold=True, color=ColorEnum.red, end_with_newline=True)
            return self.ask_for_amount_of_images()
        return int(user_choice)

    def ask_for_path(self) -> Path:
        """
        This method asks the user for the path to save the images.

        Returns:
            path (str): The path to directory provided by the user.
        """
        path = pathlib.Path(
            questionary.path(
                f"The path to save the images?", only_directories=True, default=str(pathlib.Path().absolute())
            ).ask()
        )

        if not path.is_dir():
            interactive_print(
                "Please provide a valid directory.", bold=True, end_with_newline=True, flush=True, color=ColorEnum.red
            )
            return self.ask_for_path()

        if not os.access(path, mode=os.W_OK | os.X_OK):
            interactive_print(
                f"I cannot download the images in directory '{path.absolute()}' due to insufficient permissions.",
                bold=True,
                end_with_newline=True,
                color=ColorEnum.red,
            )
            return self.ask_for_path()

        return path.absolute()

    @staticmethod
    def ask_for_confirmation(animal: AnimalAPIEndpointEnum, amount: int, path: Path) -> bool:
        """
        This method asks the user for a final confirmation for downloading the images.

        Parameters:
            animal (AnimalAPIEndpointEnum): This paramteter takes category of the animal.
            amount (int): This parameter takes the amount of images to be downloaded.
            path (pathlib.Path): This parameter takes the path pointing towards the directory
                                 where the images will be saved.

        Returns:
            confirmation (bool): The user's confirmation.
        """
        confirmation: bool = questionary.confirm(
            f"Are you sure you want to download '{amount}' images of '{animal.name}' to '{path.name}' ?",
        ).ask()
        return confirmation

    @staticmethod
    def ask_for_username() -> str:
        """
        This method asks the user for their name.

        Returns:
            confirmation (bool): The user's name, if provided, else returns the default username that is set on the
                                 user's operating system.
        """
        system_username = getpass.getuser()
        name: str = questionary.text("What is your name?", default=system_username).ask()
        if name is None:
            return system_username
        return name

    def interface(self) -> None:
        """
        This method is the main function that run catto in an interactive mode.
        """
        self.print_logo(typewriter_effect=True)
        name = self.ask_for_username()

        interactive_print(text=f"Hello, {name}.", color=ColorEnum.blue, bold=True)
        time.sleep(1)
        interactive_print(
            text=f"This is a simple program written in python that downloads random cute animals images of your choice "
            f"from the internet.",
            color=ColorEnum.blue,
            bold=True,
            end_with_newline=True,
        )
        animal = self.ask_for_animal_choice()
        amount = self.ask_for_amount_of_images()
        path = self.ask_for_path()
        user_confirm = self.ask_for_confirmation(animal=animal, amount=amount, path=path)

        if not user_confirm:
            interactive_print(
                text="Download has been cancelled by user. Exiting.",
                color=ColorEnum.red,
                bold=True,
                end_with_newline=True,
            )
            sys.exit(0)
        print("\n")
        self.client.download(animal=animal, amount=amount, path=path)
        interactive_print(
            text=f"Downloaded '{amount}' images of '{animal.name}' to directory '{path.name}' successfully!",
            color=ColorEnum.cyan,
            bold=True,
            specific_words_to_color={
                animal.name: ColorEnum.green,
                str(amount): ColorEnum.green,
                path.name: ColorEnum.green,
            },
        )
        try:
            fact = self.fetch_random_fact_about_the_selected_animal(animal)
            interactive_print(
                f"A fun fact about {animal.name}!:\n{fact}",
                color=ColorEnum.cyan,
                bold=True,
                end_with_newline=True,
                flush=True,
            )
            time.sleep(1)
        except AnimalFactNotFound:
            pass
        return
