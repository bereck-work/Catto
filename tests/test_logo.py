# -*- coding: utf-8 -*-

import re

from typer.testing import CliRunner

from src.catto import app
from src.catto.utils import ColorEnum

runner = CliRunner()


def test_logo_command():
    result = runner.invoke(app, ["logo"])
    output = re.compile(
        rf"(\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F][{[color.name for color in ColorEnum]}]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    ).sub("", str(result.stdout.strip(" ").strip("\n").lower()))
    assert result.exit_code == 0
    assert "behold the cool logo of catto: " in output
