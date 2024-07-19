from unittest.mock import patch

from typer.testing import CliRunner

from awesome_ctl_cli.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Diagnose issues using the specified connector." in result.stdout
    assert "List the available connectors for diagnostics." in result.stdout


def test_diagnose_kubernetes():
    with patch("typer.echo") as mock_echo:
        result = runner.invoke(
            app, ["diagnose", "kubernetes", "--namespace", "default"]
        )
        assert result.exit_code == 0
        mock_echo.assert_called_with(
            "Running diagnostics for Kubernetes namespace: default"
        )


def test_diagnose_unsupported_connector():
    result = runner.invoke(app, ["diagnose", "unsupported"])
    assert result.exit_code == 0
    assert "Connector 'unsupported' is not yet supported." in result.stdout


def test_list():
    with patch("typer.echo") as mock_echo:
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        mock_echo.assert_any_call("Available Connectors:")


def test_version_and_build(capsys):
    with patch("awesome_ctl_cli.cli.uvicorn.run"):
        runner.invoke(app, [])  # Invoke the CLI without any commands to show the banner

    captured = capsys.readouterr()  # Capture the output
    print(captured.out)
