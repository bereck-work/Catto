# -*- coding: utf-8 -*-
from __future__ import annotations

import getpass
import os
import pathlib
import sys
import time
from pathlib import Path

import pyfiglet
import questionary
from colorama import Fore

from ..core.api import Client
from ..utils.enums import CategoryEnum, ColorEnum
from ..utils.exceptions import CategoryFactNotFound
from ..utils.helpers import interactive_print

__all__ = ("Controller",)


class Controller:
    """
    This class is responsible for the interactive mode of the program.
    """

    def __init__(self):
        self.__client = Client()

    @staticmethod
    def print_logo(typewriter_effect: bool = False) -> str | None:
        """
        This method prints the logo of this console app, and passing True to the typewriter_effect parameter, will
        print the logo in a typewriter fashion.

        Parameters:
            typewriter_effect (bool): This parameter takes a boolean for enabling or disabling typewriter mode.
        """
        figlet_text = pyfiglet.figlet_format("Catto", font="slant")
        if typewriter_effect:
            for i in figlet_text:
                print(f"{Fore.YELLOW}{i}", end="", flush=True)
                time.sleep(0.03)
            return
        interactive_print(text=figlet_text, color=ColorEnum.yellow, bold=True)
        return figlet_text

    def fetch_random_fact_about_the_selected_animal(
        self, category: CategoryEnum
    ) -> str | None:
        """
        This method returns a random fact about the animal that the user selected.

        Parameters:
            category (CategoryEnum): This parameter takes animal that the user selected.

        Returns:
            (str | None): The fact about the animal.

        Raises:
            CategoryFactNotFound: If the APIs json response does not contain a fact about the animal.
        """
        chosen_category = CategoryEnum[category.name]
        fact = self.__client.fetch_fact_about_the_category(chosen_category)
        if fact is None:
            raise CategoryFactNotFound()
        return fact

    @staticmethod
    def ask_for_category_choice() -> CategoryEnum:
        """
        This method asks the user for the amount of images to download.

        Returns:
            (CategoryEnum): The animal that the user selected.
        """
        user_choice: str = questionary.select(
            "Select the category of animal to download: ",
            choices=[animal.name for animal in CategoryEnum],
        ).ask()
        return CategoryEnum[user_choice]

    def ask_for_amount_of_images(self) -> int:
        """
        This method asks the user for the amount of images that they want to download.

        Returns:
            (int): The amount of images to download.
        """
        user_choice = questionary.text(
            "The amount of images you want to download?", default="1"
        ).ask()
        if not user_choice.isdigit():
            interactive_print(
                "Please provide a valid integer.",
                bold=True,
                color=ColorEnum.red,
                end_with_newline=True,
            )
            return self.ask_for_amount_of_images()
        return int(user_choice)

    def ask_for_path(self) -> Path:
        """
        This method asks the user for the path to save the images.

        Returns:
            path (Path): The path to directory provided by the user.
        """
        path = pathlib.Path(
            questionary.path(
                f"The path to the directory to save the images?",
                only_directories=True,
                default=str(pathlib.Path().absolute()),
            ).ask()
        )

        if not path.is_dir():
            interactive_print(
                "Please provide a valid directory.",
                bold=True,
                end_with_newline=True,
                flush=True,
                color=ColorEnum.red,
            )
            return self.ask_for_path()

        if not os.access(path, mode=os.W_OK | os.X_OK):
            interactive_print(
                f"I cannot download the images in directory {path.absolute()} due to insufficient permissions.",
                bold=True,
                end_with_newline=True,
                color=ColorEnum.red,
                specific_words_to_color={str(path.absolute()): ColorEnum.blue},
            )
            return self.ask_for_path()

        return path.absolute()

    @staticmethod
    def ask_for_confirmation(
        category: CategoryEnum, amount: int, path: Path
    ) -> bool:
        """
        This method asks the user a final confirmation to download the images.

        Parameters:
            category (CategoryEnum): This parameter takes category of the animal.
            amount (int): This parameter takes the amount of images to be downloaded.
            path (pathlib.Path): This parameter takes the path pointing towards the directory
                                 where the images will be saved.

        Returns:
            confirmation (bool): The user's confirmation.
        """
        confirmation: bool = questionary.confirm(
            f"Are you sure you want to download '{amount}' images of '{category.name}' to '{path.name}' ?"
        ).ask()
        return confirmation

    @staticmethod
    def ask_for_username() -> str:
        """
        This method asks the user for their name.

        Returns:
            (str): The user's name, if provided, else returns the default username that is set on the
                                 user's operating system.
        """
        system_username = getpass.getuser()
        name: str = questionary.text(
            "What is your name?", default=system_username
        ).ask()
        if name is None:
            return system_username
        return name

    def interface(self) -> None:
        """
        This method is the main function that run catto in an interactive mode.
        """
        self.print_logo(typewriter_effect=True)
        name = self.ask_for_username()

        interactive_print(
            text=f"Hello, {name}.", color=ColorEnum.blue, bold=True
        )
        time.sleep(1)
        interactive_print(
            text=f"This is a simple program written in python that downloads random cute animals images of your choice "
            f"from the internet.",
            color=ColorEnum.blue,
            bold=True,
            end_with_newline=True,
        )
        category = self.ask_for_category_choice()
        amount = self.ask_for_amount_of_images()
        path = self.ask_for_path()
        user_confirm = self.ask_for_confirmation(
            category=category, amount=amount, path=path
        )

        if not user_confirm:
            interactive_print(
                text="Download has been cancelled by user. Exiting.",
                color=ColorEnum.red,
                bold=True,
                end_with_newline=True,
            )
            sys.exit(0)
        print("\n")
        self.__client.download(animal=category, amount=amount, path=path)
        interactive_print(
            text=f"Downloaded {amount} images of {category.name} to directory {path.name} successfully!",
            color=ColorEnum.cyan,
            bold=True,
            specific_words_to_color={
                category.name: ColorEnum.blue,
                str(amount): ColorEnum.blue,
                path.name: ColorEnum.blue,
            },
        )

        try:
            fact = str(self.fetch_random_fact_about_the_selected_animal(category))
            interactive_print(
                f"A fun fact about {category.name}!:\n{fact}",
                color=ColorEnum.cyan,
                bold=True,
                end_with_newline=True,
                flush=True,
                specific_words_to_color={
                    fact: ColorEnum.green.underline
                },
            )
            time.sleep(1)
        except CategoryFactNotFound:
            pass
        return
