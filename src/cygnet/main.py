import typer
import importlib.metadata

app = typer.Typer(help="Cygnet: a simple C compiler in Python")

@app.command()
def clitest():
    """A test command to verify the CLI is working."""
    typer.echo("Cygnet CLI is working!")

@app.command()
def build():
    pass

@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        is_eager=True,
    )
):
    if version:
        typer.echo(importlib.metadata.version("cygnet"))
        raise typer.Exit()

if __name__ == "__main__":
    app()