from typer.testing import CliRunner

from src.catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["show-all-animals"])
    assert result.exit_code == 0
    assert "all animals supported by catto" in result.stdout.strip(" ").strip("\n").lower()
