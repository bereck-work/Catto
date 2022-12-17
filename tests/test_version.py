# -*- coding: utf-8 -*-

import re

from typer.testing import CliRunner
import typer

from src.catto import app, __version__
from src.catto.utils import ColorEnum

runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])
    output = re.compile(
        rf"(\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F][{[color.name for color in ColorEnum]}]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    ).sub("", str(result.stdout.strip(" ").strip("\n").lower()))
    assert result.exit_code == 0
    assert "version table" in output
    assert typer.__version__ in output and __version__ in output
