import random
from typing import Union, Dict

from rich.console import Console

from .enums import ColorEnum

__all__ = (
    "interactive_print",
    "ExponentialBackoff",
)


def interactive_print(
    text: str,
    color: ColorEnum,
    flush: bool = False,
    bold: bool = False,
    end_with_newline: bool = False,
    specific_words_to_color: Dict[str, ColorEnum] = None,
) -> None:
    """
    This function pretty-prints text in the terminal, it can print text in a typewriter fashion,
    with a specified color and the text can be in bold.

    Parameters:
        text (str): This parameter takes the text that needs to be printed in the terminal.

        color (ColorEnum): This parameter takes the color of the text that needs to be printed.

        flush (bool): This parameter takes a boolean value, if set to True, the text will be printed immediately.

        bold (bool): This parameter takes a boolean which sets the text to be displayed as bold. Default: False.

        end_with_newline (bool): This parameter takes a boolean which sets the text to be printed at the end of the
                                line with a newline character. Default: False.

        specific_words_to_color (typing.Dict[str, ColorEnum]): This parameter takes a dictionary of specifc words to be
                                                               seperately colored, the keys are the words and
                                                               the values are the colors.
    """
    console = Console()

    if bold and specific_words_to_color is not None:
        for word, color in specific_words_to_color.items():
            text = text.replace(word, f"[{color.value}]{word}")

        console.print(
            f"[bold][{color.value}]{text}", new_line_start=end_with_newline, end="\n" if end_with_newline else ""
        )
        print(flush=flush)
        return

    if bold and specific_words_to_color is None:
        console.print(
            f"[bold][{color.value}]{text}", new_line_start=end_with_newline, end="\n" if end_with_newline else ""
        )
        print(flush=flush)
        return

    if not bold:
        console.print(f"[{color.value}]{text}", new_line_start=end_with_newline, end="\n" if end_with_newline else "")
        print(flush=flush)
        return

    return


class ExponentialBackoff:
    """
    This class implements an exponential backoff algorithm. An exponential backoff algorithm is a form of closed-loop
    control system that reduces the rate of a controlled process in response to adverse events. Each time an adverse
    event is encountered, the rate of the process is reduced by some multiplicative factor. Examples of adverse
    events include collisions of network traffic, an error response from a service, or an explicit request to reduce
    the rate (i.e. "back off").
    """

    def __init__(
        self,
        *,
        base: Union[float, int] = 1,
        maximum_time: Union[int, float] = 30.0,
        maximum_tries: Union[int, float, None] = 5,
    ):
        """
        Parameters:
            base (typing.Union[int, float]): The base time to multiply exponentially. Default: 1.
            maximum_time (Union[int, float]): This parameter takes the  maximum time in seconds to wait. Defaults to 30.0
            maximum_tries (Union[int, float, None]): This parameter takes the amount of times to backoff before resetting.
                                                     If set to None, backoff will run indefinitely. Default: 5.
        """
        self.__base = base
        self.__maximum_time = maximum_time
        self.__maximum_tries = maximum_tries
        self.__retries: int = 1
        self.__inner_random = random.Random()  # A custom random object so that we can seed it.
        self.__inner_random.seed()

        self.__last_wait: float = 0

    def calculate(self) -> float:
        """
        This method calculates the time to wait. It returns the time to wait in seconds.

        Returns:
            (float): The next wait time.
        """
        exponent = min((self.__retries**2), self.__maximum_time)
        wait = self.__inner_random.uniform(0, (self.__base * 2) * exponent)

        if wait <= self.__last_wait:
            wait = self.__last_wait * 2

        self.__last_wait = wait

        if wait > self.__maximum_time:
            wait = self.__maximum_time
            self.__reset()

        if self.__maximum_tries and self.__retries >= self.__maximum_tries:
            self.__reset()

        self.__retries += 1

        return wait

    def __reset(self) -> None:
        """
        This method resets the exponential backoff. It sets the retries to 0 and the last time wait to 0.
        This method is called when the maximum tries is reached, and should not be called manually.
        """
        self.__retries = 0
        self.__last_wait = 0
        return
