from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["logo"])
    assert result.exit_code == 0
    assert "Behold the cool logo of catto: " in result.stdout
