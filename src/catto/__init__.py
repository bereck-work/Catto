import click
from colorama import Fore

from catto.core.downloader import Client
from catto.core.interactive import Controller

controller = Controller()
client = Client()


@click.group(
    name="catto",
    help="Catto is a simple tool that downloads random cute animal images of your choice from the internet.",
)
def main_command_interface():
    """
    This function is the main command interface for the catto package.
    """
    main_command_interface.add_command(catto_cli)
    main_command_interface.add_command(interactive_cli)


@main_command_interface.command(
    name="download", help="Download cute animal images from the internet."
)
@click.option(
    "--category",
    help=f"Choose between different animals categories to download images from.\nCategories are: "
    f"{', '.join(list(client.animal_category_dict.keys()))}. Default is 'cats'.",
    default="cats",
)
@click.option(
    "--amount", help="Amount of images to download.", metavar="<int>", default=1
)
@click.option("--path", help="Output directory to save the images to.")
def catto_cli(category, amount, path):
    confirm = controller.ask_for_confirmation()
    if not confirm:
        click.echo(
            f"{controller.bold_color}{Fore.RED} Download cancelled by user. {Fore.RESET}"
        )
        return
    controller.typewriter(
        f"Downloading {amount} images of {category} to {path}....",
        color=Fore.BLUE,
        bold=True,
        speed=0.05,
    )
    client.download(category, amount, path)
    controller.typewriter(
        text=f"Downloaded {amount} images of {category} to {path} successfully!",
        speed=0.05,
        color=Fore.GREEN,
        bold=True,
    )
    controller.typewriter(
        text="Thank you for using Catto!", speed=0.05, color=Fore.BLUE, bold=True
    )
    controller.typewriter(
        text="Have a nice day!", speed=0.05, color=Fore.BLUE, bold=True
    )


@main_command_interface.command(
    "interactive", help="Run catto in interactive mode. Try it and see!"
)
def interactive_cli():
    controller.start_interactive_mode()


if __name__ == "__main__":
    main_command_interface()
