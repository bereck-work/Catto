# -*- coding: utf-8 -*-

from __future__ import annotations

__version__ = "1.0.5"
__name__ = "catto"
__all__ = ("__version__", "__name__", "app")

import sys
import time
from pathlib import Path

import httpx
import typer
from rich.console import Console
from rich.table import Table
from typer import Typer

from .core.api import Client
from .core.interactive import Controller
from .utils.enums import CategoryEnum, ColorEnum
from .utils.exceptions import CategoryFactNotFound
from .utils.helpers import (
    interactive_print,
    check_internet_connection,
    ExponentialBackoff,
)

console = Console(color_system="truecolor", soft_wrap=True, force_terminal=True)
controller = Controller()
client = Client()

app = Typer(
    name="catto",
    help="Catto is a simple tool that downloads random cute animal images, gifs or videos "
    "of your choice from the internet.",
    context_settings=dict(help_option_names=["-h", "--help", "-help"]),
    no_args_is_help=True,
)


@app.command(
    name="download",
    help="Use this command to download cute animal images manually in a command line fashion.",
)
def download_command(
    category: str = typer.Option(
        help=f"Choose between different animals categories to download images from.\nCategories are: "
        f"{', '.join([animal.name for animal in CategoryEnum])}.",
        default="cats",
        rich_help_panel="Secondary Arguments",
    ),
    amount: int = typer.Option(
        min=1,
        max=100,
        default=1,
        help="Pass the amount of animal images to be downloaded.",
    ),
    path: str = typer.Option(
        help="Pass the directory where the images will be downloaded.",
        exists=True,
        default=Path.cwd(),
    ),
) -> dict[str, Path | list[str]] | None:
    """
    This function is the command "catto download" for manually downloading images from the internet.
    """
    directory = Path(path)
    table = Table(title="Downloading images...")
    table.add_column("Category", style="bold")
    table.add_column("Amount", style="bold")
    table.add_column("Directory", style="bold")
    table.add_column("Path", style="bold")
    table.add_row(
        category, str(amount), directory.name, str(directory.absolute())
    )
    console.print(table)

    data = client.download(
        animal=CategoryEnum[category.lower()], amount=amount, path=directory
    )
    if len(data["names"]) == 0:
        return

    interactive_print(
        text=f"Downloaded {amount} images of {category} in {directory.name} successfully!",
        color=ColorEnum.green,
        bold=True,
        end_with_newline=True,
        specific_words_to_color={
            str(amount): ColorEnum.blue,
            category: ColorEnum.blue,
            directory.name: ColorEnum.blue,
        },
    )
    return data


@app.command(
    "interactive", help="Run catto in interactive mode. Try it and see!"
)
def interactive_command() -> None:
    """
    This function is the command "catto interactive" for running catto in interactive mode.
    """
    try:
        controller.interface()
    except KeyboardInterrupt:
        interactive_print(
            f"[*] User has interrupted the program. Exiting gracefully.",
            bold=True,
            color=ColorEnum.red,
            end_with_newline=True,
        )
        typer.Exit()
    return


@app.command("version", help="Print the version of catto.")
def version_command() -> None:
    """
    This function is the command "catto version" for printing the version of catto.
    """
    entries = {
        "Catto": f"v{__version__}",
        "Python": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}-"
        f"{sys.version_info.releaselevel}",
        "httpx": f"v{httpx.__version__}",
        "Typer": f"v{typer.__version__}",
    }

    table = Table(title="Version Table")

    table.add_column("No.", style=ColorEnum.cyan.value)
    table.add_column("Package", style=ColorEnum.magenta.value)
    table.add_column("Version", style=ColorEnum.green.value)
    for index, item in enumerate(entries.keys(), start=1):
        table.add_row(f"{index}.)", item, entries[item])

    console.print(table)
    return


@app.command(
    "status",
    help="Check the status of each animal API endpoint, Catto is currently using.",
)
def status_command() -> None:
    """
    This function is the command "catto status" that shows the status of each API endpoint, Catto uses for
    downloading images.
    """
    endpoints = [str(e.value) for e in CategoryEnum]
    backoff = ExponentialBackoff(base=0.05)
    table = Table(title="Endpoint Statuses.")

    table.add_column("No.", style=ColorEnum.cyan.value, no_wrap=True)
    table.add_column("Endpoints", style=ColorEnum.magenta.value)
    table.add_column("Status", justify="right", style=ColorEnum.green.value)
    table.add_column("Message", justify="right", style=ColorEnum.green.value)

    table_data: list[dict[str, str]] = list()

    for endpoint in endpoints:
        try:
            with httpx.Client(timeout=30.0) as _client:
                response = _client.get(endpoint)
                table_data.append(
                    {
                        "endpoint": endpoint,
                        "reason": response.reason_phrase,
                        "status_code": str(response.status_code),
                    }
                )

            time.sleep(backoff.calculate())

        except Exception as e:
            interactive_print(
                f"Exception occurred while making an GET HTTP request to {endpoint}:\n{e}",
                color=ColorEnum.red,
                bold=True,
                end_with_newline=True,
                specific_words_to_color={endpoint: ColorEnum.blue},
            )
            continue

    for index, data in enumerate(table_data, start=1):
        table.add_row(
            f"{index}.)",
            data.get("endpoint"),
            data.get("status_code"),
            data.get("reason"),
        )
    console.print(table)
    return


@app.command(
    "show-all-categories", help="This command shows all the categories of animals."
)
def all_categories_command() -> list[CategoryEnum]:
    """
    This function is the command "catto show-all-categories" that shows the status of each API endpoint.
    """
    endpoints = [e for e in CategoryEnum]
    table = Table(title="All available animal categories.")
    table.add_column("No.", style=ColorEnum.cyan.value, no_wrap=True)
    table.add_column("Animal", style=ColorEnum.magenta.value)
    table.add_column("Endpoints", justify="right", style=ColorEnum.green.value)

    for index, endpoint in enumerate(endpoints, start=1):
        table.add_row(
            f"{index}.)",
            endpoint.name,
            str(endpoint.value),
        )

    console.print(table)
    return endpoints


@app.command(name="logo", help="Print the catto logo.")
def logo_command(typewriter: bool = typer.Option(
        default=False,
        help="Pass the amount of animal images to be downloaded.")) -> str | None:
    """
    This function is the command "catto logo" for printing the catto logo.
    """
    interactive_print(
        text="Behold the cool logo of catto: ",
        bold=True,
        color=ColorEnum.cyan,
        end_with_newline=True,
    )
    return controller.print_logo(typewriter_effect=typewriter)


@app.command(name="fact", help="Get a fun fact about the specified animal.")
def fact_command(
    category: str = typer.Option(
        help=f"Choose between different animals categories to download images from.\nCategories are: "
        f"{', '.join([animal.name for animal in CategoryEnum])}.",
        default="cats",
        rich_help_panel="Secondary Arguments",
    )
) -> str | None:
    """
    This function is the command "catto fact" that prints a random fact about the specified animal.
    """
    animal = CategoryEnum[category.lower()]
    try:
        fact = controller.fetch_random_fact_about_the_selected_animal(animal)
        interactive_print(
            f"A fun fact about {animal.name}!:\n{fact}",
            color=ColorEnum.cyan,
            bold=True,
            end_with_newline=True,
            flush=True,
            specific_words_to_color={
                animal.name: ColorEnum.green,
                fact: ColorEnum.magenta,
            },
        )
        return fact
    except CategoryFactNotFound:
        interactive_print(
            f"Sorry, no fact returned for '{animal.name}' by the API.",
            color=ColorEnum.red,
            bold=True,
            end_with_newline=True,
            specific_words_to_color={animal.name: ColorEnum.blue},
        )
        return


@app.callback()
def app_command_callback_middleware(context: typer.Context):
    """
    This function is called when a command is invoked.
    """
    if context.invoked_subcommand.lower() == "version" or context.invoked_subcommand == "logo" or \
            context.invoked_subcommand == "show-all-categories":
        return

    if not check_internet_connection():
        interactive_print(
            f"[*] Command {context.invoked_subcommand}"
            f"requires an internet connection to operate. Aborted!",
            color=ColorEnum.red,
            end_with_newline=True,
            bold=True,
            specific_words_to_color={
                str(context.invoked_subcommand): ColorEnum.blue
            },
        )
        sys.exit(1)

    return
