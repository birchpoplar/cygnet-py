from pathlib import Path
import subprocess
import os
from rich import print
from .lexer import Lexer
from .parser import Parser, print_ast_out
from .codegen import TackyToAssembly 
from .tackygen import TackyGenerator, print_tacky
from .print import print_source_code, print_msg, print_error, print_token_list
from .errors import CompilerError
from .enums import SUCCESS, FAIL, CompileStage, PrintFlags


# Compiler driver functions

def compile_driver(path: Path, stage: CompileStage, print_flags: PrintFlags):

    # Preprocess file, bug out if failure
    # TODO: improve preprocess file error generation
    if preprocess_file(path) != SUCCESS:
        return FAIL

    result = SUCCESS
    try:
        run_pipeline(path, stage, print_flags)
    except CompilerError as e:
        print_error(str(e))
        result = FAIL
    finally:
        cleanup_files(path, stage)

    return result


def run_pipeline(path: Path, stage: CompileStage, print_flags: PrintFlags):

    # 1. Read preprocessed source
    preproc_file = path.with_suffix(".i")
    source = read_lines(preproc_file)
    if print_flags.source:
        print_source_code(source)

    # 2. Lexer
    print_msg("INFO", "Lexing file...")
    lexer = Lexer(source)
    tokens = lexer.lex()
    if print_flags.tokens:
        print_token_list(tokens)
    if stage == CompileStage.LEX:
        return

    # 3. Parser
    print_msg("INFO", "Parsing file...")
    parser = Parser(tokens)
    ast = parser.parse()
    if print_flags.ast:
        print_ast_out(ast, 0)
    if stage == CompileStage.PARSE:
        return

    # 4. TACKY Generation
    print_msg("INFO", "Generating TACKY...")
    tacky_gen = TackyGenerator(ast)
    ir = tacky_gen.generate()
    if print_flags.tacky:
        print_tacky(ir)
    if stage == CompileStage.TACKY:
        return

    # 5. Code Generation
    print_msg("INFO", "Generating Assembly...")
    codegen = CodeGenerator(ir)
    codegen_ir = codegen.generate()
    if print_flags.ir:
        print(ir)

    # 5b. Emit assembly text
    emitter = Emitter(codegen_ir)
    emitter.emit_program(codegen_ir)
    assembly = emitter.get_assembly()
    
    if print_flags.asm:
        print(assembly)
    if stage == CompileStage.CODEGEN:
        return

    # 6. Write Assembly File (needed for ASSEMBLE & LINK)
    print_msg("INFO", "Writing assembly file...")
    asm_file = path.with_suffix(".s")
    asm_file.write_text(assembly)
    if stage == CompileStage.ASSEMBLE:
        return
    
    # 7. Link
    link_file(path)
    return
        

def cleanup_files(path: Path, stage: CompileStage):
    # Always delete .i
    preproc_file = path.with_suffix(".i")
    if preproc_file.exists():
        print_msg("INFO", "Deleting preprocessed file...")
        preproc_file.unlink()

    # Delete .s unless we stopped at ASSEMBLE or CODEGEN
    if stage not in (CompileStage.ASSEMBLE, CompileStage.CODEGEN):
        asm_file = path.with_suffix(".s")
        if asm_file.exists():
            print_msg("INFO", "Deleting assembly file...")
            asm_file.unlink()

        
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


def link_file(path: Path):

    assembly_file = path.with_suffix(".s")
    output_executable = path.with_suffix("")

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
