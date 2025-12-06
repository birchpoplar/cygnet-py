from pathlib import Path
import subprocess
import os

# Compiler driver functions

def compile_driver(path: Path, mode: str):
    preprocess_file(path, mode)
    if mode != "default":
        part_compile_file(path, mode)
    else:
        compile_file(path, mode)

def preprocess_file(path: Path, mode: str):
    print("Preprocessing file...")

    source_file = path
    preproc_file = path.with_suffix(".i")
    
    result = subprocess.run(
        ["gcc", "-E", "-P", source_file, "-o", preproc_file],
        capture_output=True,
        text=True,
        check=True
        )

    return result.returncode

def part_compile_file(path: Path, mode: str):
    print("Part compiling file...")

    if mode == "lex":
        print("Lexing file...")
        pass
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

    return
    
def compile_file(path: Path, mode: str):
    print("Compiling file...")

    source_file = path
    
    result = subprocess.run(
        ["gcc", "-S", "-O", "-fno-asynchronous-unwind-tables", "-fcf-protection=none", source_file],
        capture_output=True,
        text=True,
        check=True
        )

    # Delete preprocessed file if it exists
    preproc_file = path.with_suffix(".i")

    if os.path.exists(preproc_file):
        print("Deleting preprocessed file...")
        os.remove(preproc_file)

    # Delete assembly file if it exists
    assembly_file = path.with_suffix(".s")

    if os.path.exists(assembly_file):
        print("Deleting assembly file...")
        os.remove(assembly_file)
        
    return result.returncode
