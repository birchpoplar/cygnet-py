import typer
from typing import Optional
from pathlib import Path
from .enums import CompileStage, PrintFlags
from .driver import compile_driver

app = typer.Typer(help="Cygnet: a simple C compiler in Python")

@app.callback(invoke_without_command=True)
def build(
        path: Optional[Path] = typer.Argument(None, help="C source file to compile"),
        assemble: bool = typer.Option(False, "-S", help="Generate assembly only"),
        lex: bool = typer.Option(False, "--lex", help="Run lexer only"),
        parse: bool = typer.Option(False, "--parse", help="Run lexer and parser only"),
        tacky: bool = typer.Option(False, "--tacky", help="Stop after TACKY generation"),
        codegen: bool = typer.Option(False, "--codegen", help="Run lexer, parser and assembly generation"),
        print_source: bool = typer.Option(False, "--print-source", "-p", help="Print source lines"),
        print_tokens: bool = typer.Option(False, "--print-tokens", "-t", help="Print tokens"),
        print_ast: bool = typer.Option(False, "--print-ast", "-a", help="Print AST"),
        print_tacky: bool = typer.Option(False, "--print-tacky", "-k", help="Print TACKY"),
        print_ir: bool = typer.Option(False, "--print-ir", "-r", help="Print IR"),
        print_asm: bool = typer.Option(False, "--print-asm", "-m", help="Print assembly"),
        ):
    if path is None:
        typer.echo("Error: no source file provided")
        raise typer.Exit(1)    

    # Map compile stage flags to enum
    if lex:
        stage = CompileStage.LEX
    elif parse:
        stage = CompileStage.PARSE
    elif tacky:
        stage = CompileStage.TACKY
    elif codegen:
        stage = CompileStage.CODEGEN
    elif assemble:
        stage = CompileStage.ASSEMBLE
    else:
        stage = CompileStage.LINK

    # Build print flags enum from CLI
    print_flags = PrintFlags(
        source = print_source,
        tokens = print_tokens,
        ast = print_ast,
        tacky = print_tacky,
        ir = print_ir,
        asm = print_asm
    )
        
    result = compile_driver(path, stage, print_flags)

    if result == 0:
        raise typer.Exit(0)
    else:
        raise typer.Exit(1)
    
if __name__ == "__main__":
    app()
