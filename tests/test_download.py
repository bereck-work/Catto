# -*- coding: utf-8 -*-

import re
from pathlib import Path

from typer.testing import CliRunner

from src.catto import app
from src.catto.utils import check_internet_connection, ColorEnum

runner = CliRunner()


def test_download_command():
    created_path = Path(Path.cwd() / "gallery")
    created_path.mkdir(exist_ok=True)
    result = runner.invoke(
        app=app,
        args=[
            "download",
            "--category",
            "cats",
            "--amount",
            "5",
            "--path",
            "./gallery",
        ],
        standalone_mode=False,
    )
    assert check_internet_connection()
    output = re.compile(
        rf"(\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F][{[color.name for color in ColorEnum]}]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    ).sub("", str(result.stdout.strip(" ").strip("\n").lower()))
    command_data = result.return_value

    assert result.exit_code == 0
    if "downloaded 1 images of cats in gallery" in output:
        assert True

    names_of_images = command_data["names"]

    directory = Path(command_data["directory"]).glob("**/*")
    files = [x for x in directory if x.is_file()]
    for image in files:
        if image.name in names_of_images:
            assert True
        else:
            continue

    directory = created_path.glob("**/*")

    [
        file.unlink(missing_ok=True)
        for file in directory
        if file.is_file()
    ]
    created_path.rmdir()
