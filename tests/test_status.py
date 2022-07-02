from typer.testing import CliRunner

from src.catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "endpoints" in result.stdout.strip(" ").strip("\n").lower()
