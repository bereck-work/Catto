from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Version Table" in result.stdout
