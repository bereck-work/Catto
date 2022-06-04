import random
import typing
from typing import Optional

from rich.console import Console

__all__ = (
    "interactive_print",
    "ExponentialBackoff",
)


def interactive_print(
    text: str,
    color: str,
    flush: bool = False,
    bold: bool = False,
    end_with_newline: bool = False,
    specific_words_to_color: dict = None,
) -> None:
    """
    This function pretty-prints text in the terminal, it can print text in a typewriter fashion,
    with a specified color and the text can be in bold.

    Parameters:
        text (str): This parameter takes the text that needs to be printed in the terminal.
        color (str): This parameter takes the color of the text that needs to be printed. ASCII colors are supported
                     only. It is recommended to use the colors from the colorama module.
        flush (bool): This parameter takes a boolean value, if set to True, the text will be printed immediately.
        bold (bool): This parameter takes a boolean which sets the text to be bold, Default: False.
        end_with_newline (bool): This parameter takes a boolean which sets the text to be printed at the end of the
                                line with a newline character. Default: False.
        specific_words_to_color (dict): This parameter takes a dictionary of words to color, the keys are the words
                                        and the values are the colors.
    """
    console = Console()
    if bold and specific_words_to_color is not None:
        for word, color in specific_words_to_color.items():
            text = text.replace(word, f"[{color}]{word}")

        console.print(f"[bold][{color}]{text}", new_line_start=end_with_newline)
        print(flush=flush)
    if bold and specific_words_to_color is None:
        console.print(f"[bold][{color}]{text}", new_line_start=end_with_newline)
        print(flush=flush)
    if not bold:
        console.print(f"[{color}]{text}", new_line_start=end_with_newline)
        print(flush=flush)
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
        self, *, base: typing.Union[float, int] = 1, maximum_time: float = 30.0, maximum_tries: Optional[int] = 5
    ):
        """
        Parameters
        ----------
        base: int
            The base time to multiply exponentially. Defaults to 1.
        maximum_time: float
            The maximum wait time. Defaults to 30.0
        maximum_tries: Optional[int]
            The amount of times to backoff before resetting. Defaults to 5. If set to None,
            backoff will run indefinitely.
        """
        self._base = base
        self._maximum_time = maximum_time
        self._maximum_tries = maximum_tries
        self._retries: int = 1

        rand = random.Random()
        rand.seed()

        self._rand = rand.uniform

        self._last_wait: float = 0

    def calculate(self) -> float:
        """
        This method calculates the next wait time.

        Returns
        -------
        float
            The next wait time.
        """
        exponent = min((self._retries**2), self._maximum_time)
        wait = self._rand(0, (self._base * 2) * exponent)

        if wait <= self._last_wait:
            wait = self._last_wait * 2

        self._last_wait = wait

        if wait > self._maximum_time:
            wait = self._maximum_time
            self._retries = 0
            self._last_wait = 0

        if self._maximum_tries and self._retries >= self._maximum_tries:
            self._retries = 0
            self._last_wait = 0

        self._retries += 1

        return wait
