import getpass
import os
import pathlib
import sys
import time

import loguru
import pyfiglet
import questionary
from colorama import Fore, Style

from catto.core.downloader import Client


class Controller:
    """
    This class is responsible for the interactive mode of the program.
    """

    def __init__(self):
        self.client = Client()
        self.logger = loguru.logger
        self.bold_color = "\033[1m"

    def typewriter(self, text, speed=0.05, color=Fore.GREEN, bold=False):
        """
        This method prints text in a typewriter fashion.

        Args:
            text (str): The text to print.
            speed (float): The speed of the typewriter.
            color (str): The color of the text.
            bold (bool): Whether the text should be bold. Default: False.
        """
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

    def ask_for_animal_choice(self) -> str:
        """
        This method asks the user for the amount of images to download.

        Returns:
            animal_choice (str): The user's choice of animal.
        """
        user_choice = questionary.select(
            "Select the category of animal...",
            choices=list(self.client.animal_category_dict.keys()),
        ).ask()
        return user_choice

    def print_logo(self):
        """
        This method prints the logo of the application.
        """
        figlet_text = pyfiglet.figlet_format("Catto", font="slant")
        self.typewriter(figlet_text, speed=0.01, color=Fore.YELLOW, bold=True)
        return

    def get_random_fact_about_the_selected_animal(self, animal: str) -> str:
        """
        This method prints the logo of the application.
        """
        animal_type = self.client.animal_category_dict[animal]
        fact = self.client.get_fact_about_the_animal(animal_type)
        return fact

    def ask_for_amount_of_images(self) -> int:
        """
        This method asks the user for the amount of images to download.

        Returns:
            amount_of_images (int): The user's choice of amount of images.
        """
        user_choice = questionary.text(
            "The amount of images you want to download?",
        ).ask()
        if not user_choice.isdigit():
            print(
                f"{self.bold_color}{Fore.RED} Please provide a valid integer. {Style.RESET_ALL}"
            )
            return self.ask_for_amount_of_images()
        return int(user_choice)

    def ask_for_path(self) -> str:
        """
        This method asks the user for the path to save the images.

        Returns:
            path (str): The user's choice of path.
        """
        parent_path = pathlib.Path(os.getcwd()).name
        path = questionary.path(
            f"The path to save the images?",
            only_directories=True,
            default=f"./{parent_path}",
        ).ask()
        if not pathlib.Path(path).is_dir():
            print(
                f"{self.bold_color}{Fore.RED} Please provide a valid directory. {Style.RESET_ALL}"
            )
            return self.ask_for_path()
        if not os.access(path, mode=os.W_OK | os.X_OK):
            print(
                f"{self.bold_color}{Fore.RED} I cannot download the images on the directory due to insufficient "
                f"permissions. {Style.RESET_ALL}"
            )
            return self.ask_for_path()
        return path

    @staticmethod
    def ask_for_confirmation() -> bool:
        """
        This method asks the user for confirmation for downloading the images.

        Returns:
            confirmation (bool): The user's confirmation.
        """
        confirmation = questionary.confirm(
            "Are you sure you want to download these images?"
        ).ask()
        return confirmation

    @staticmethod
    def ask_for_username():
        """
        This method asks the user for their name.

        Returns:
            confirmation (bool): The user's choice of confirmation.
        """
        system_username = getpass.getuser()
        name = questionary.text("What is your name?", default=system_username).ask()
        return name

    def interface(self):
        """
        This method is the main function that run catto in an interactive mode.
        """
        self.print_logo()
        name = self.ask_for_username()
        self.typewriter(text=f"Hello, {name}! ", speed=0.05, color=Fore.BLUE, bold=True)
        time.sleep(1)
        self.typewriter(
            text=f"This is a simple program written in python "
            f"that downloads random cute animals images of your choice from the internet.",
            speed=0.05,
            color=Fore.BLUE,
            bold=True,
        )
        user_choice = self.ask_for_animal_choice()
        amount = self.ask_for_amount_of_images()
        path = self.ask_for_path()
        user_confirm = self.ask_for_confirmation()
        if not user_confirm:
            print(f"{self.bold_color}{Fore.RED} Download cancelled. {Style.RESET_ALL}")
            return
        self.typewriter(text="Downloading...", speed=0.05, color=Fore.BLUE, bold=True)
        self.client.download(user_choice, amount, path)
        self.typewriter(
            text=f"Downloaded {amount} images of {user_choice} to directory {path} successfully!",
            speed=0.05,
            color=Fore.CYAN,
            bold=True,
        )
        fact = self.get_random_fact_about_the_selected_animal(user_choice)
        print(f"{self.bold_color}{Fore.CYAN}A fun fact about {user_choice}!\n{Fore.GREEN}{fact} {Style.RESET_ALL}")
        time.sleep(1)
        self.typewriter(
            text="Thank you for using Catto!", speed=0.05, color=Fore.BLUE, bold=True
        )
        self.typewriter(text="Have a nice day!", speed=0.05, color=Fore.BLUE, bold=True)

    def start_interactive_mode(self):
        """
        This method starts :meth:`interface`.
        """
        try:
            self.interface()
        except KeyboardInterrupt:
            print(f"{self.bold_color}{Fore.RED}[*] Exiting... {Style.RESET_ALL}")
            sys.exit(0)

        except SystemExit:
            print(f"{self.bold_color}{Fore.RED}[*] Exiting... {Style.RESET_ALL}")
            sys.exit(0)
