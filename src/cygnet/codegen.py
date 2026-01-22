from dataclasses import dataclass
from typing import List
from enum import Enum, auto
from . import tackygen as tacky
from .errors import TackyAssemblyError


# Tacky to Assembly Nodes, abstract base classes

@dataclass
class TackyAssemblyNode:
    pass


class Reg(Enum):
    AX = auto()
    R10 = auto()


@dataclass
class Operand(TackyAssemblyNode):
    pass


@dataclass
class UnaryOperator(TackyAssemblyNode):
    pass


@dataclass
class Instruction(TackyAssemblyNode):
    pass


@dataclass
class Function(TackyAssemblyNode):
    name: str
    instructions: List[Instruction]


@dataclass
class Program(TackyAssemblyNode):
    function: 'Function'


# Derived node classes

@dataclass
class Neg(UnaryOperator):
    pass


@dataclass
class Not(UnaryOperator):
    pass


@dataclass
class Mov(Instruction):
    op_src: Operand
    op_dst: Operand


@dataclass
class AllocateStack(Instruction):
    value: int

    
@dataclass
class Unary(Instruction):
    unary_op: UnaryOperator
    operand: Operand

    
@dataclass
class Ret(Instruction):
    pass


@dataclass
class Pseudo(Operand):
    identifier: str


@dataclass
class Stack(Operand):
    offset: int
    

@dataclass
class Imm(Operand):
    value: int


@dataclass
class Register(Operand):
    reg: Reg

    
class TackyToAssembly:
    def __init__(self, tacky_root: tacky.Program):
        self.tacky_root = tacky_root


    # Tacky to assembly functions
    def generate(self):
        return self.generate_program(self.tacky_root)
        
    def generate_program(self, tacky_program):
        function = self.generate_function(tacky_program.function)
        return Program(function=function)

    def generate_function(self, tacky_function):
        instructions = []
        for tacky_insn in tacky_function.body:
            asm_insns = self.convert_instruction(tacky_insn)
            instructions.extend(asm_insns)
        return Function(tacky_function.identifier, instructions)

    def convert_instruction(self, tacky_insn):
        asm_insns = []
        if isinstance(tacky_insn, tacky.Return):
            asm_insns.append(Mov(self.convert_val(tacky_insn.val), Register(Reg.AX))) 
            asm_insns.append(Ret())
        elif isinstance(tacky_insn, tacky.Unary):
            asm_insns.append(Mov(self.convert_val(tacky_insn.src), self.convert_val(tacky_insn.dst)))
            asm_insns.append(Unary(self.convert_unary_op(tacky_insn.unary_op), self.convert_val(tacky_insn.dst)))
        else:
            raise TackyAssemblyError("Error processing assembly from TACKY", tacky_insn)
        return asm_insns
            
    def convert_val(self, val):
        pass

    
    def convert_unary_op(self, unary_op):
        pass
            
    
    # def generate_statement(self, tacky_statement):
    #     instructions = []
    #     if isinstance(tacky_statement, Return):
    #         operand = self.generate_exp(tacky_statement.expr)
    #         instructions.append(Mov(operand, Register(reg=Reg.AX)))
    #         instructions.append(Ret())
    #         return instructions
        
    # def generate_exp(self, tacky_exp):
    #     if isinstance(tacky_exp, Constant):
    #         return Imm(value=ast_exp.value)
    #     raise TackyAssemblyError(f"Unexpected expression type", ast_exp)


