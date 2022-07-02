from typer.testing import CliRunner

from src.catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["logo"])
    assert result.exit_code == 0
    assert "hehold the cool logo of catto: " in result.stdout.lower().strip(" ").strip("\n")
