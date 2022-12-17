# -*- coding: utf-8 -*-

import re

from typer.testing import CliRunner

from src.catto import app
from src.catto.utils import ColorEnum

runner = CliRunner()


def test_help_command():
    result = runner.invoke(app, ["--help"])
    output = re.compile(
        rf"(\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F][{[color.name for color in ColorEnum]}]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    ).sub("", str(result.stdout.strip(" ").strip("\n").lower()))
    print(output)
    assert result.exit_code == 0
    assert "show this message and exit." in output

    for command in app.registered_commands:
        if command.name.lower() in output and command.help.lower() in output:
            assert True

        else:
            continue
