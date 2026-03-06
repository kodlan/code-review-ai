from typer.testing import CliRunner

from code_review_ai.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Review the current Git diff" in result.output


def test_review_runs():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "not yet implemented" in result.output
