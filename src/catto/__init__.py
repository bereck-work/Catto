import sys

import click
from colorama import Fore, Style

from .core.downloader import Client
from .core.interactive import Controller

controller = Controller()
client = Client()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "-help"])


@click.group(
    name="catto",
    help="Catto is a simple tool that downloads random cute animal images of your choice from the internet.",
    context_settings=CONTEXT_SETTINGS,
)
def main_command_interface():
    """
    This function is the main command interface for the catto package.
    """
    main_command_interface.add_command(catto_cli)
    main_command_interface.add_command(interactive_cli)
    return


@main_command_interface.command(name="download", help="Download cute animal images from the internet.")
@click.option(
    "--category",
    help=f"Choose between different animals categories to download images from.\nCategories are: "
    f"{', '.join(list(client.animal_category_dict.keys()))}. Default is 'cats'.",
    default="cats",
)
@click.option("--amount", help="Amount of images to download.", metavar="<int>", default=1)
@click.option("--path", help="Output directory to save the images to.", metavar="<path>", default=click.Path())
@click.option(
    "--typewriter",
    help="Enable or disable the typewriter effect. Default is set to false.",
    metavar="<bool>",
    default=False,
)
def catto_cli(category: str, amount: int, path: str, typewriter: bool):
    """
    This function is the command "catto --download" for manually downloading images from the internet.
    """
    controller.interactive_print(
        f"Downloading {amount} images of {category} to {path}....",
        color=Fore.BLUE,
        bold=True,
        speed=0.05,
        typewriter=typewriter,
    )
    client.download(animal=category, amount=amount, directory=path)
    controller.interactive_print(
        text=f"Downloaded {amount} images of {category} to {path} successfully!",
        speed=0.05,
        color=Fore.GREEN,
        bold=True,
        typewriter=typewriter,
    )
    controller.interactive_print(
        text="Thank you for using Catto!", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter
    )
    controller.interactive_print(text="Have a nice day!", speed=0.05, color=Fore.BLUE, bold=True, typewriter=typewriter)
    return


@main_command_interface.command("interactive", help="Run catto in interactive mode. Try it and see!")
@click.option(
    "--typewriter",
    help="Enable or disable the typewriter effect. Default is set to false.",
    metavar="<bool>",
    default=False,
)
def interactive_cli(typewriter: bool):
    """
    This function is the command "catto --interactive" for running catto in interactive mode.
    """
    try:
        controller.interface(typewriter_mode=typewriter)
    except KeyboardInterrupt:
        print(f"{controller.bold_color}{Fore.RED}[*] Exiting... {Style.RESET_ALL}")
        sys.exit(0)

    except SystemExit:
        print(f"{controller.bold_color}{Fore.RED}[*] Exiting... {Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main_command_interface()
