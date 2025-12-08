from pathlib import Path
import subprocess
import os
from rich import print
from .lexer import lexer

# Compiler driver functions

def compile_driver(path: Path, mode: str):
    preprocess_file(path)
    part_compile = False
    
    if mode in ("lex", "parse", "codegen"):

        part_compile = True
        
        result = part_compile_file(path, mode)

        if result == 0:
            pass
        else:
            return 1
        
    else:
        result = compile_file(path)
        
        if result == 0:
            pass
        else:
            return 1

    if mode != "assemble":
        if not part_compile:
            link_file(path)

    return 0
    
def preprocess_file(path: Path):

    source_file = path
    preproc_file = path.with_suffix(".i")

    print(f"[green]Preprocessing file[/green] : {source_file}")

    try:
        result = subprocess.run(
            ["gcc", "-E", "-P", source_file, "-o", preproc_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Preprocessing failed:\n{e.stderr}")
        return 1

    return 0

def part_compile_file(path: Path, mode: str):
    print("Part compiling file...")

    if mode == "lex":
        print("Lexing file...")
        lexer(path)
        
    elif mode == "parse":
        print("Parsing file...")
        pass
    elif mode == "codegen":
        print("Generating code...")
        pass
    else:
        # Shouldn't get here
        print("Doing nothing!")
        pass

    # Delete preprocessed file if it exists
    preproc_file = path.with_suffix(".i")

    if os.path.exists(preproc_file):
        print("Deleting preprocessed file...")
        os.remove(preproc_file)

    return 0

def compile_file(path: Path):

    source_file = path

    print(f"[green]Compiling file[/green] : {source_file}")
    
    try:
        result = subprocess.run(
            ["gcc", "-S", "-O", "-fno-asynchronous-unwind-tables", "-fcf-protection=none", source_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed:\n{e.stderr}")
        return 1

    print(f"[green]Assembly file created[/green] : {source_file.with_suffix('.s')}")

    cleanup_preprocessed(path)
    
    return 0

def link_file(path: Path):

    assembly_file = path.with_suffix(".s")
    output_executable = path.stem

    print(f"[green]Linking file[/green] : {assembly_file}")

    try:
        result = subprocess.run(
            ["gcc", assembly_file, "-o", output_executable],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Linking failed:\n{e.stderr}")
        return 1

    cleanup_assembly(path)

    print(f"[green]Output executable generated[/green] : {output_executable}")
    
    return 0

def cleanup_preprocessed(path: Path):
    preproc_file = path.with_suffix(".i")

    if os.path.exists(preproc_file):
        print("[blue]Deleting preprocessed file...[/blue]")
        os.remove(preproc_file)
    

def cleanup_assembly(path: Path):
    assembly_file = path.with_suffix(".s")

    if os.path.exists(assembly_file):
        print("[blue]Deleting assembly file...[/blue]")
        os.remove(assembly_file)
