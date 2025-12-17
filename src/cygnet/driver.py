from pathlib import Path
import subprocess
import os
from rich import print
from .lexer import lexer
from .print import print_source_code, print_msg, print_error
from .errors import CompilerError
from .enums import SUCCESS, FAIL

# Compiler driver functions

def compile_driver(path:  Path, mode: str, print_source: bool = False, print_tokens: bool = False):
        
    result = preprocess_file(path)
    if result != SUCCESS:
        return FAIL

    part_compile = False

    try:
    
        if mode in ("lex", "parse", "codegen"):

            part_compile = True
        
            result = part_compile_file(path, mode, print_source, print_tokens)

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
    
    except CompilerError as e:
        print_error(str(e))
        return 1
        
    if mode != "assemble":
        if not part_compile:
            link_file(path)
            
    return 0
    
def preprocess_file(path: Path):

    source_file = path
    preproc_file = path.with_suffix(".i")

    print_msg("INFO", f"Preprocessing file : {path}") 

    try:
        result = subprocess.run(
            ["gcc", "-E", "-P", source_file, "-o", preproc_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print_error(f"Preprocessing failed : {e.stderr}")
        return 1

    return 0

def read_lines(path: Path):
    with open(path, 'r') as f:
        lines = f.readlines()

    stripped_lines = [line.strip() for line in lines]

    return stripped_lines

def part_compile_file(path: Path, mode: str, print_source: bool = False, print_tokens: bool = False):
    print_msg("INFO", "Part compiling file...")

    source_code = read_lines(path)
    result = 0
    
    if print_source:
        print_source_code(source_code)

    try:
        
        if mode == "lex":
            print_msg("INFO", "Lexing file...")
            result = lexer(source_code, print_tokens)
        
        elif mode == "parse":
            print("Parsing file...")
            pass
        elif mode == "codegen":
            print("Generating code...")
            pass
        else:
            # Shouldn't get here
            print("Doing nothing!")
            return 1

    finally:  
        # Delete preprocessed file if it exists
        preproc_file = path.with_suffix(".i")
        
        print(preproc_file)
        
        if os.path.exists(preproc_file):
            print_msg("INFO", "Deleting preprocessed file...")
            os.remove(preproc_file)

    return 0

def compile_file(path: Path):

    source_file = path

    print_msg("INFO", f"Compiling file : {source_file}")
    
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

    print_msg("INFO", f"Assembly file created : {source_file.with_suffix('.s')}")

    cleanup_preprocessed(path)
    
    return 0

def link_file(path: Path):

    assembly_file = path.with_suffix(".s")
    output_executable = path.stem

    print_msg("INFO", f"Linking file : {assembly_file}")

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

    print_msg("INFO", f"Output executable generated : {output_executable}")
    
    return 0

def cleanup_preprocessed(path: Path):
    preproc_file = path.with_suffix(".i")

    if os.path.exists(preproc_file):
        print_msg("INFO", "Deleting preprocessed file...")
        os.remove(preproc_file)
    

def cleanup_assembly(path: Path):
    assembly_file = path.with_suffix(".s")

    if os.path.exists(assembly_file):
        print_msg("INFO", "Deleting assembly file...")
        os.remove(assembly_file)
