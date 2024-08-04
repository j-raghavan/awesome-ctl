import sys
import time
from threading import Thread

import typer
import uvicorn
from pyfiglet import figlet_format
from rich.console import Console
from rich.table import Table

from awesome_ctl import __build_number__, __version__
from awesome_ctl.utils import list_connectors

app = typer.Typer()
console = Console()


def start_ui():
    uvicorn.run("awesome_ctl.ui.ui:app", host="127.0.0.1", port=4200)


def start_api():
    uvicorn.run("awesome_ctl.api.main:app", host="127.0.0.1", port=8000)


@app.command()
def diagnose(
    ctx: typer.Context,
    connector: str = typer.Argument(
        ..., help="The connector to use for diagnostics (e.g., 'kubernetes')"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Diagnose issues using the specified connector.
    """
    if verbose:
        typer.echo("Running in verbose mode")

    ui_server_thread = Thread(target=start_ui)
    ui_server_thread.daemon = True
    ui_server_thread.start()

    api_server_thread = Thread(target=start_api)
    api_server_thread.daemon = True
    api_server_thread.start()

    if connector == "kubernetes":
        typer.echo("Running diagnostics for Kubernetes")
        # ... (Your Kubernetes diagnostics logic will go here)
    # elif connector == "docker":
    #     # ... (Docker diagnostics logic)
    # elif connector == "aws":
    #     # ... (AWS diagnostics logic)
    else:
        typer.echo(f"\nConnector '{connector}' is not yet supported.")
        typer.echo("\nPlease choose one of the available connectors:")
        list_command()
        sys.exit(1)

    typer.echo("")
    typer.echo("  You can access awesome-ctl UI at http://127.0.0.1:4200")
    typer.echo("")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down...")
        ui_server_thread.join()  # Allow the UI server thread to finish
        api_server_thread.join()  # Allow the API server thread to finish


@app.command(name="list")
def list_command():
    """
    List the available connectors for diagnostics.
    """
    connectors = list_connectors()

    typer.echo("")
    table = Table(
        title=str(),
        title_justify="left",
        show_header=True,
        header_style="bold magenta",
        border_style="white",
    )
    table.add_column("Available Connectors", justify="left", style="cyan", no_wrap=True)
    for connector in connectors:
        table.add_row(connector, style="sandy_brown", end_section=True)

    console.print(table, justify="left")
    typer.echo("")


@app.callback()
def callback():
    """Awesome Command Line Interface to interact with Awesome Client"""
    banner = figlet_format("awesome - ctl", font="standard", width=80, justify="center")
    typer.echo("")
    typer.secho(banner, fg=typer.colors.BRIGHT_WHITE, bold=True)
    typer.echo("")
    typer.secho(f"  Version: \t {__version__}", fg=typer.colors.BRIGHT_BLUE, bold=True)
    typer.secho(
        f"  Build: \t {__build_number__}", fg=typer.colors.BRIGHT_BLUE, bold=True
    )


def main(args=None):
    app.add_typer(typer.Typer(callback=diagnose), name="d", hidden=True)
    app.add_typer(typer.Typer(callback=list_command), name="l", hidden=True)
    app(args)


if __name__ == "__main__":
    main(args=sys.argv[1:])
