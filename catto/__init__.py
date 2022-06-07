import sys
from pathlib import Path

import requests
import typer
from rich.table import Table

from .core.downloader import Client
from .core.interactive import Controller
from .utils.enums import AnimalAPIEndpointEnum, ColorEnum
from .utils.helpers import interactive_print

controller = Controller()
client = Client()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-help"])

app = typer.Typer(
    name="catto",
    help="Catto is a simple tool that downloads random cute animal images, gifs or videos "
    "of your choice from the internet.",
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    add_completion=True,
)


@app.command(
    name="download", help="Use this command to download cute animal images manually in a command line fashion."
)
def catto_download_command(
    category: str = typer.Option(
        help=f"Choose between different animals categories to download images from.\nCategories are: "
        f"{', '.join([animal.name for animal in AnimalAPIEndpointEnum])}.",
        default="cats",
        show_default=True,
    ),
    amount: int = typer.Option(min=1, max=100, default=..., help="Pass the amount of animal images to be downloaded."),
    path: str = typer.Option(
        help="Pass the directory where the images will be downloaded.", exists=True, dir_okay=True, default=...
    ),
) -> None:
    """
    This function is the command "catto download" for manually downloading images from the internet.
    """
    directory = Path(path)
    table = Table(title="Downloading images...")
    table.add_column("Category", style="bold", no_wrap=True)
    table.add_column("Amount", style="bold", no_wrap=True)
    table.add_column("Directory", style="bold", no_wrap=True)
    table.add_column("Path", style="bold", no_wrap=True)
    table.add_row(category, str(amount), directory.name, str(directory.absolute()))
    controller.console.print(table)

    client.download(animal=AnimalAPIEndpointEnum[category.lower()], amount=amount, path=directory)
    interactive_print(
        text=f"Downloaded '{amount}' images of '{category}' in '{directory.name}' successfully!",
        color=ColorEnum.green,
        bold=True,
        end_with_newline=True,
        specific_words_to_color={
            str(amount): ColorEnum.green,
            category: ColorEnum.green,
            directory.name: ColorEnum.green,
        },
    )
    return


@app.command("interactive", help="Run catto in interactive mode. Try it and see!")
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
        typer.Exit(0)


@app.command("version", help="Print the version of catto.")
def version_command() -> None:
    """
    This function is the command "catto --version" for printing the version of catto.
    """
    entries = {
        "Catto": f"v{client.version}",
        "Python": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}-"
        f"{sys.version_info.releaselevel}",
        "requests": f"v{requests.__version__}",
        "Typer": f"v{typer.__version__}",
    }

    table = Table(title="Version Table")

    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Package", style="magenta")
    table.add_column("Version", justify="right", style=ColorEnum.green.value)

    for key, value in entries.items():
        i = key.index(key) + 1
        table.add_row(f"{str(i)}.)", key, value)

    controller.console.print(table)
    return


@app.command("status", help="Check the status of each animal API endpoint, Catto is currently using.")
def status_command() -> None:
    """
    This function is the command "catto status" that shows the status of each API endpoint, Catto uses for
    downloading images.
    """
    endpoints = [e.value for e in AnimalAPIEndpointEnum]
    table = Table(title="Endpoint Statuses.")

    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Endpoints", style="magenta")
    table.add_column("Status", justify="right", style=ColorEnum.green.value)
    table.add_column("Message", justify="right", style=ColorEnum.green.value)

    for endpoint in endpoints:
        try:
            i = endpoints.index(endpoint) + 1
            response = requests.get(endpoint)
            table.add_row(f"{str(i)}.)", endpoint, str(response.status_code), response.reason)
        except Exception as e:
            interactive_print(
                f"Exception occurred while making an GET HTTP request to {endpoint}:\n{e}",
                color=ColorEnum.blue,
                bold=True,
                end_with_newline=True,
                specific_words_to_color={endpoint: ColorEnum.red},
            )
    controller.console.print(table)
    return


@app.command("show-all-animals", help="This command shows all the categories of animals.")
def all_animals_command() -> None:
    """
    This function is the command "catto show-all-animals" that shows the status of each API endpoint.
    """
    endpoints = [e for e in AnimalAPIEndpointEnum]
    table = Table(title="All Animals Supported by Catto.")
    table.add_column("No.", style=ColorEnum.cyan.value, no_wrap=True)
    table.add_column("Animal", style=ColorEnum.magenta.value)
    table.add_column("Endpoints", justify="right", style=ColorEnum.green.value)

    for endpoint in endpoints:
        i = endpoints.index(endpoint) + 1
        table.add_row(f"{str(i)}.)", endpoint.name, endpoint.value)

    controller.console.print(table)
    return


@app.command(name="logo", help="Print the catto logo.")
def logo_command():
    """
    This function is the command "catto logo" for printing the catto logo.
    """
    controller.print_logo(typewriter_effect=True)
    return
