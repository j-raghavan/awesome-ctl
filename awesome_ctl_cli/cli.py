import os
import sys
from threading import Thread
from typing import Optional

import typer
import uvicorn
from pyfiglet import figlet_format

from awesome_ctl import __build_number__, __version__

app = typer.Typer()

@app.command()
def diagnose(ctx: typer.Context,
             connector: str = typer.Argument(..., help="The connector to use for diagnostics (e.g., 'kubernetes')"),
             namespace: Optional[str] = typer.Option(None, "--namespace", "-n", help="The Kubernetes namespace to analyze (only for Kubernetes connector)"),
             ):
    """
    Diagnose issues using the specified connector.
    """
    if connector == "kubernetes":
        typer.echo(f"Running diagnostics for Kubernetes namespace: {namespace}")
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
    """ Awesome Command Line Interface to interact with Awesome Client"""
    banner = figlet_format("awesome - ctl", font="standard", width=80, justify="center")
    typer.echo("")
    typer.secho(banner, fg=typer.colors.BRIGHT_WHITE, bold=True)
    typer.echo("")
    typer.secho(f"  Version:  {__version__}", fg=typer.colors.BRIGHT_BLUE, bold=True)
    typer.secho(
        f"  Build: {__build_number__}", fg=typer.colors.BRIGHT_BLUE, bold=True
    )

    typer.echo("")

    typer.echo(
        f"  You can access awesome-ctl at http://127.0.0.1:4200"
    )
    typer.echo("")

    def run_server():
        uvicorn.run("awesome_ctl.api.main:app", host="127.0.0.1", port=4200)

    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

def main(args = None):
    app(args)

if __name__ == "__main__":
    main(args = sys.argv[1:])