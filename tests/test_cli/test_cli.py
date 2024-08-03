import pytest

from unittest.mock import patch


from typer.testing import CliRunner

from awesome import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Diagnose issues using the specified connector." in result.stdout
    assert "List the available connectors for diagnostics." in result.stdout


@pytest.mark.skip(reason="Not implemented yet")
def test_diagnose_kubernetes():
    with patch("typer.echo") as mock_echo:
        result = runner.invoke(
            app, ["diagnose", "kubernetes", "--namespace", "default"]
        )
        assert result.exit_code == 0
        mock_echo.assert_called_with(
            "Running diagnostics for Kubernetes namespace: default"
        )


@pytest.mark.skip(reason="Not implemented yet")
def test_diagnose_unsupported_connector():
    result = runner.invoke(app, ["diagnose", "unsupported"])
    assert result.exit_code == 0
    assert "Connector 'unsupported' is not yet supported." in result.stdout


@pytest.mark.skip(reason="Not implemented yet")
def test_list():
    with patch("typer.echo") as mock_echo:
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        mock_echo.assert_any_call("Available Connectors:")


@pytest.mark.skip(reason="Not implemented yet")
def test_version_and_build(capsys):
    with patch("awesome.run_server"):
        runner.invoke(app, [])  # Invoke the CLI without any commands to show the banner

    captured = capsys.readouterr()  # Capture the output
    print(captured.out)
