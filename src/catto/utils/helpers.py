# -*- coding: utf-8 -*-
import random
import socket

from rich.console import Console

from .enums import ColorEnum

__all__ = (
    "interactive_print",
    "ExponentialBackoff",
    "check_internet_connection",
)


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
        base: float | int = 1,
        maximum_time: float | int = 30.0,
        maximum_tries: float | int | None = 5,
    ):
        """
        Parameters:
            base (int | float): The base time to multiply exponentially. Default: 1.
            maximum_time (int | float): This parameter takes the  maximum time in seconds to wait.
                                              Defaults to 30.0
            maximum_tries (int | float | None]): This parameter takes the amount of times to backoff before
                                                     resetting. If set to None, backoff will run indefinitely.
                                                     Default: 5.
        """
        self.__base = base
        self.__maximum_time = maximum_time
        self.__maximum_tries = maximum_tries
        self.__retries: int = 1
        self.__inner_random = (
            random.Random()
        )
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


def interactive_print(
    text: str,
    color: ColorEnum = ColorEnum.white,
    flush: bool = False,
    bold: bool = False,
    end_with_newline: bool = False,
    specific_words_to_color: dict[str, ColorEnum] = None,
) -> None:
    """
    This function pretty-prints text in the terminal, it can print text in a typewriter fashion,
    with a specified color and the text can be in bold.

    Parameters:
        text (str): This parameter takes the text that needs to be printed in the terminal.

        color (ColorEnum): This parameter takes the color, which the text will be used to colored with entirely.

        flush (bool): This parameter takes a boolean value, where the terminal buffer will be flushed or not.
                      Default: False

        bold (bool): This parameter takes a boolean which sets the text to be displayed as bold. Default: False.

        end_with_newline (bool): This parameter takes a boolean which sets the text to be printed at the end of the
                                line with a newline character. Default: False.

        specific_words_to_color (dict[str, ColorEnum]): This parameter takes a dictionary of specific words to be
                                                               separately colored, the keys are the words and
                                                               the values are the colors.
    """
    console = Console(
        color_system="truecolor", soft_wrap=True, force_terminal=True
    )
    if specific_words_to_color is not None:
        words = text.split(" ")
        for word in words:
            if word in specific_words_to_color.keys():
                words[
                    words.index(word)
                ] = f"[{specific_words_to_color.get(word)}]{word}"
            else:
                words[words.index(word)] = f"[{color}]{word}"

        final_text = "".join(words)

        if bold:
            console.print(f"[bold] {final_text}")
            print(flush=flush, end="\n" if end_with_newline else None)
            return
        else:
            console.print(final_text)
            print(flush=flush, end="\n" if end_with_newline else None)
            return

    if bold:
        console.print(f"[bold][{color}]{text}")
        print(flush=flush, end="\n" if end_with_newline else None)
        return
    else:
        console.print(f"[{color}]{text}")
        print(flush=flush, end="\n" if end_with_newline else None)
        return


def check_internet_connection() -> bool:
    """
    This function checks if the user has an internet connection.

    Returns:
        (bool): True if the user has an internet connection, False otherwise.
    """
    try:
        host = socket.gethostbyname("one.one.one.one")
        socket.create_connection((host, 80), 2).close()
        return True
    except socket.gaierror:
        return False
