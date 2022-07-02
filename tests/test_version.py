from typer.testing import CliRunner

from src.catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "version table" in result.stdout.lower().strip("\n").strip(" ")
