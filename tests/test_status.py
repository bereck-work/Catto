from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Endpoints" in result.stdout
