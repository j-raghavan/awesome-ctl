import sys
import time
from threading import Thread

import typer
import uvicorn
from pyfiglet import figlet_format

from awesome_ctl import __build_number__, __version__

app = typer.Typer()


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

    if connector == "kubernetes":
        typer.echo("Running diagnostics for Kubernetes")
        # ... (Your Kubernetes diagnostics logic will go here)
    # elif connector == "docker":
    #     # ... (Docker diagnostics logic)
    # elif connector == "aws":
    #     # ... (AWS diagnostics logic)
    else:
        typer.echo(f"Connector '{connector}' is not yet supported.")


@app.command()
def list():
    """
    List the available connectors for diagnostics.
    """
    typer.echo("Available Connectors:")
    # ... (Logic to retrieve and print available connectors)


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

    typer.echo("")

    typer.echo("  You can access awesome-ctl UI at http://127.0.0.1:4200")
    typer.echo("")

    def run_server():
        uvicorn.run("awesome_ctl.ui.ui:app", host="127.0.0.1", port=4200)

    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down...")
        server_thread.join()  # Allow the server thread to finish

def main(args=None):
    app(args)


if __name__ == "__main__":
    main(args=sys.argv[1:])
