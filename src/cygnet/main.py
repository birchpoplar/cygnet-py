import typer
from typing import Optional
from pathlib import Path
from .driver import compile_driver

app = typer.Typer(help="Cygnet: a simple C compiler in Python")

@app.callback(invoke_without_command=True)
def build(
        path: Optional[Path] = typer.Argument(None, help="C source file to compile"),
        assemble: bool = typer.Option(False, "-S", help="Generate assembly only"),
        lex: bool = typer.Option(False, "--lex", help="Run lexer only"),
        parse: bool = typer.Option(False, "--parse", help="Run lexer and parser only"),
        codegen: bool = typer.Option(False, "--codegen", help="Run lexer, parser and assembly generation"),
        print_source: bool = typer.Option(False, "--print-source", "-p", help="Print source lines"),
        print_tokens: bool = typer.Option(False, "--print-tokens", "-t", help="Print tokens"),
        print_ast: bool = typer.Option(False, "--print-ast", "-a", help="Print AST"),
        print_ir: bool = typer.Option(False, "--print-ir", "-r", help="Print IR"),
        print_asm: bool = typer.Option(False, "--print-asm", "-m", help="Print assembly"),
        ):
    if path is None:
        typer.echo("Error: no source file provided")
        raise typer.Exit(1)    

    if assemble:
        mode = "assemble"
    elif lex:
        mode = "lex"
    elif parse:
        mode = "parse"
    elif codegen:
        mode = "codegen"
    else:
        mode = "default"

    result = compile_driver(path, mode, print_source=print_source, print_tokens=print_tokens, print_ast=print_ast, print_ir=print_ir, print_asm=print_asm)

    if result == 0:
        raise typer.Exit(0)
    else:
        raise typer.Exit(1)
    
if __name__ == "__main__":
    app()
