from typer.testing import CliRunner

from catto import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["show-all-animals"])
    assert result.exit_code == 0
    assert "All Animals Supported by Catto" in result.stdout.strip(" ").strip("\n")
