import getpass
import os
import pathlib
import time
from typing import Optional

import loguru
import pyfiglet
import questionary
from colorama import Fore, Style

from ..core.downloader import Client
from ..utils import AnimalFactNotFound


class Controller:
    """
    This class is responsible for the interactive mode of the program.
    """

    def __init__(self):
        self.client = Client()
        self.logger = loguru.logger
        self.bold_color = "\033[1m"

    def interactive_print(self, text: str, typewriter: bool, speed=0.05, color=Fore.GREEN, bold=False):
        """
        This method pretty prints text in the terminal.

        Args:
            text (str): The text to print.
            speed (float): The speed of the typewriter effect, if enabled.
            color (str): The color of the text.
            bold (bool): Whether the text should be bold. Default: False.
            typewriter (bool): Whether the text should be printed with a typewriter effect. Default: False.
        """
        if typewriter is True:
            for char in text:
                if bold:
                    print(f"{self.bold_color}{color}{char}", end="", flush=True)
                    time.sleep(speed)
                    if ", " in char:
                        time.sleep(0.03)
                else:
                    print(f"{color}{char}", end="", flush=True)
                    time.sleep(speed)
                    if ", " in char:
                        time.sleep(0.03)
            print("\n\n", end="", flush=True)
        else:
            if bold:
                print(f"{self.bold_color}{color}{text}", end="", flush=True)
                print("\n\n", end="", flush=True)
            else:
                print(f"{color}{text}", end="", flush=True)
                print("\n\n", end="", flush=True)
        return

    def ask_for_animal_choice(self) -> str:
        """
        This method asks the user for the amount of images to download.

        Returns:
            animal_choice (str): The user's choice of animal.
        """
        user_choice: str = questionary.select(
            "Select the category of animal...", choices=list(self.client.animal_category_dict.keys())
        ).ask()
        return user_choice

    def print_logo(self, typewriter_mode: bool) -> None:
        """
        This method prints the logo of the application.

        Args:
            typewriter_mode (bool): Whether the logo should be printed with a typewriter effect.
        """
        figlet_text = pyfiglet.figlet_format("Catto", font="slant")
        self.interactive_print(figlet_text, speed=0.01, color=Fore.YELLOW, bold=True, typewriter=typewriter_mode)
        return

    def get_random_fact_about_the_selected_animal(self, animal: str) -> Optional[str]:
        """
        This method returns a random fact about the animal that the user selected.

        Args:
            animal (str): The animal that the user selected.

        Returns:
            fact (Optional[str]): The fact about the animal.

        Raises:
            AnimalFactNotFound: If the animal does not have any facts or the API is not able to return any facts.
        """
        animal_type = self.client.animal_category_dict[animal]
        fact = self.client.get_fact_about_the_animal(animal_type)
        if fact is None:
            raise AnimalFactNotFound()
        return fact

    def ask_for_amount_of_images(self) -> int:
        """
        This method asks the user for the amount of images to download.

        Returns:
            amount_of_images (int): The user's choice of amount of images.
        """
        user_choice = questionary.text(
            "The amount of images you want to download?",
            default="5",
        ).ask()
        if not user_choice.isdigit():
            print(f"{self.bold_color}{Fore.RED} Please provide a valid integer. {Style.RESET_ALL}")
            return self.ask_for_amount_of_images()
        return int(user_choice)

    def ask_for_path(self) -> str:
        """
        This method asks the user for the path to save the images.

        Returns:
            path (str): The user's choice of path.
        """
        parent_path = pathlib.Path().resolve().name
        path = questionary.path(f"The path to save the images?", only_directories=True, default=parent_path).ask()
        if not pathlib.Path(path).is_dir():
            print(f"{self.bold_color}{Fore.RED} Please provide a valid directory. {Style.RESET_ALL}")
            return self.ask_for_path()
        if not os.access(path, mode=os.W_OK | os.X_OK):
            print(
                f"{self.bold_color}{Fore.RED} I cannot download the images on the directory due to insufficient "
                f"permissions. {Style.RESET_ALL}"
            )
            return self.ask_for_path()
        return path

    @staticmethod
    def ask_for_confirmation(category: str, amount: int, directory: str) -> bool:
        """
        This method asks the user for confirmation for downloading the images.

        Args:
            category (str): The category of the animal.
            amount (int): The amount of images to be downloaded.
            directory (str): The path to save the images.

        Returns:
            confirmation (bool): The user's confirmation.
        """
        confirmation: bool = questionary.confirm(
            f"Are you sure you want to download {amount } of {category} images to {directory}?",
        ).ask()
        return confirmation

    @staticmethod
    def ask_for_username() -> str:
        """
        This method asks the user for their name.

        Returns:
            confirmation (bool): The user's choice of confirmation.
        """
        system_username = getpass.getuser()
        name: str = questionary.text("What is your name?", default=system_username).ask()
        return name

    def interface(self, typewriter_mode: bool) -> None:
        """
        This method is the main function that run catto in an interactive mode.

        Args:
            typewriter_mode (bool): Disable or enable typewriter mode.
        """
        self.print_logo(typewriter_mode=typewriter_mode)
        name = self.ask_for_username()
        if name is None:
            self.logger.error("The user did not provide a name.")
            return

        self.interactive_print(
            text=f"Hello, {name}! ", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter_mode
        )
        time.sleep(1)
        self.interactive_print(
            text=f"This is a simple program written in python "
            f"that downloads random cute animals images of your choice from the internet.",
            speed=0.05,
            color=Fore.BLUE,
            bold=True,
            typewriter=typewriter_mode,
        )
        user_choice = self.ask_for_animal_choice()
        amount = self.ask_for_amount_of_images()
        path = self.ask_for_path()
        user_confirm = self.ask_for_confirmation(category=user_choice, amount=amount, directory=path)

        if not user_confirm:
            print(f"{self.bold_color}{Fore.RED} Download cancelled. {Style.RESET_ALL}")
            return

        self.interactive_print(
            text="Downloading...", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter_mode
        )
        self.client.download(user_choice, amount, path)
        self.interactive_print(
            text=f"Downloaded {amount} images of {user_choice} to directory {path} successfully!",
            speed=0.05,
            color=Fore.CYAN,
            bold=True,
            typewriter=typewriter_mode,
        )
        try:
            fact = self.get_random_fact_about_the_selected_animal(user_choice)
            print(
                f"{self.bold_color}{Fore.CYAN}A fun fact about {user_choice}!\n{Fore.GREEN}{fact} {Style.RESET_ALL}\n\n"
            )
            time.sleep(1)
        except AnimalFactNotFound:
            pass
        self.interactive_print(
            text="Thank you for using Catto!", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter_mode
        )
        self.interactive_print(
            text="Have a nice day!", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter_mode
        )
        return
