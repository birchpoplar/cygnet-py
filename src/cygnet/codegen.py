from dataclasses import dataclass
from typing import List
from .parser import ASTNode, Return, Constant
from .errors import CodeGenError


# Code Generation Nodes, abstract base classes

@dataclass
class CodeGenNode:
    pass


@dataclass
class Operand(CodeGenNode):
    pass


@dataclass
class Instruction(CodeGenNode):
    pass


@dataclass
class Function(CodeGenNode):
    name: str
    instructions: List[Instruction]


@dataclass
class Program(CodeGenNode):
    function: 'Function'


# Derived node classes

@dataclass
class Mov(Instruction):
    op_src: Operand
    op_dst: Operand


@dataclass
class Ret(Instruction):
    pass


@dataclass
class Imm(Operand):
    value: int


@dataclass
class Register(Operand):
    name: str

    
class CodeGenerator:
    def __init__(self, ast_root: ASTNode):
        self.ast_root = ast_root


    # Code generation functions
    def generate(self):
        return self.generate_program(self.ast_root)
        
    def generate_program(self, ast_program):
        function = self.generate_function(ast_program.function)
        return Program(function=function)

    def generate_function(self, ast_function):
        body = self.generate_statement(ast_function.body)
        return Function(ast_function.identifier, body)

    def generate_statement(self, ast_statement):
        instructions = []
        if isinstance(ast_statement, Return):
            operand = self.generate_exp(ast_statement.expr)
            instructions.append(Mov(operand, Register(name='eax')))
            instructions.append(Ret())
            return instructions
        
    def generate_exp(self, ast_exp):
        if isinstance(ast_exp, Constant):
            return Imm(value=ast_exp.value)
        raise CodeGenError(f"Unexpected expression type", ast_exp)


class Emitter:
    def __init__(self, code_root: Program):
        self.code_root = code_root
        self.assembly_lines = []
        self.indent = 4

    def emit_program(self, program):
        self.emit_function(program.function)
        
    def emit_function(self, function):
        indentation = " "*self.indent 
        self.assembly_lines.append(self._emit_comment("Function", function))
        self.assembly_lines.append(f"{indentation}.globl {function.name}")
        self.assembly_lines.append(f"{function.name}:")
        for instruction in function.instructions:
            self.emit_instruction(instruction)

        self.assembly_lines.append("# Confirm code does not require executable stack")
        self.assembly_lines.append(".section .note.GNU-stack,\"\",@progbits")
            
    def emit_instruction(self, instruction):
        if isinstance(instruction, Ret):
            self._emit_insn("ret")
        elif isinstance(instruction, Mov):
            self._emit_insn("movl", instruction.op_src, instruction.op_dst)
        
    def get_assembly(self):
        return "\n".join(self.assembly_lines)

    def _emit_comment(self, type, object):
        return f"# {type}: {object}"
    
    def _emit_insn(self, mnemonic, *operands):
        indentation = " "*self.indent
        formatted_ops = [self._format_operand(op) for op in operands]
        operands_str = ", ".join(formatted_ops)
        if operands_str:
            line = f"{indentation}{mnemonic} {operands_str}"
        else:
            line = f"{indentation}{mnemonic}"
        self.assembly_lines.append(self._emit_comment("Instruction", formatted_ops))
        self.assembly_lines.append(line)

    def _format_operand(self, operand):
        if isinstance(operand, Imm):
            return f"${operand.value}"
        elif isinstance(operand, Register):
            return f"%{operand.name}"
        raise CodeGenError(f"Unexpected operand type", operand)
