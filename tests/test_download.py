from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["download", "--category", "cats", "--amount", 1, "--path", "./tests/test_gallery"])
    assert result.exit_code == 0
    assert "Downloaded '1' images of 'cats' in 'test_gallery'" in result.stdout.strip(" ").strip("\n")
