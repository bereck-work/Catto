from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.stdout.strip(" ").strip("\n")
