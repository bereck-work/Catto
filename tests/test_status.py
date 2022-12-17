# -*- coding: utf-8 -*-

import re
import time

from typer.testing import CliRunner
from src.catto.utils.enums import CategoryEnum, ColorEnum
from src.catto.utils.helpers import (
    check_internet_connection,
    ExponentialBackoff,
)
import httpx
from src.catto import app

runner = CliRunner()


def test_status_command():
    result = runner.invoke(app, ["status"])
    backoff = ExponentialBackoff(base=0.05)
    output = re.compile(
        rf"(\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F][{[color.name for color in ColorEnum]}]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    ).sub("", str(result.stdout.strip(" ").strip("\n").lower()))
    endpoints = [str(animal.value) for animal in CategoryEnum]
    assert check_internet_connection()
    assert result.exit_code == 0
    assert (
        "endpoint statuses." in output
        and "status" in output
        and "message" in output
    )
    for url in endpoints:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
        time.sleep(backoff.calculate())
    assert (
        response.reason_phrase.lower() in output
        and str(response.status_code) in output
    )
