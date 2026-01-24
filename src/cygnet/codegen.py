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
            raise TackyAssemblyError("Error processing instruction from TACKY", tacky_insn)
        return asm_insns
            
    def convert_unary_op(self, tacky_unary_op):
        if isinstance(tacky_unary_op, tacky.Complement):
            return Not()
        elif isinstance(tacky_unary_op, tacky.Negate):
            return Neg()
        else:
            raise TackyAssemblyError("Error processing unary operator from TACKY", tacky_unary_op)    
    
    def convert_val(self, tacky_val):
        if isinstance(tacky_val, tacky.Constant):
            return Imm(tacky_val.value)
        elif isinstance(tacky_val, tacky.Var):
            return Pseudo(tacky_val.identifier)
        else:
            raise TackyAssemblyError("Error processing value from TACKY", tacky_val)    
            
class PseudoReplacer:
    def __init__(self, asm_root: Program):
        self.asm_root = asm_root

    # Tacky to assembly functions
    def replace(self):
        return self.replace_program(self.asm_root)

    def replace_program(self, asm_program):
        function = self.replace_function(asm_program.function)
        return Program(function=function)
    
    def replace_function(self, asm_function):
        self.pseudo_map = {}
        self.stack_offset = 0
        cnv_asm_insns = []
        for asm_insn in asm_function.instructions:
            cnv_asm_insn = self.replace_instruction(asm_insn)
            cnv_asm_insns.append(cnv_asm_insn)
        return Function(asm_function.name, cnv_asm_insns)

    def replace_instruction(self, asm_insn):
        if isinstance(asm_insn, Mov):
            return Mov(self.replace_operand(asm_insn.op_src), self.replace_operand(asm_insn.op_dst))
        elif isinstance(asm_insn, Ret):
            return Ret()
        elif isinstance(asm_insn, Unary):
            return Unary(asm_insn.unary_op, self.replace_operand(asm_insn.operand))
        else:
            raise TackyAssemblyError("Error replacing instruction", asm_insn)
            
    def replace_operand(self, asm_op): 
        if isinstance(asm_op, Pseudo):
            if asm_op.identifier not in self.pseudo_map:
                self.stack_offset += -4
                self.pseudo_map[asm_op.identifier] = self.stack_offset
            return Stack(offset=self.pseudo_map[asm_op.identifier])
        elif isinstance(asm_op, (Imm, Register)):
            return asm_op
        else:
            raise TackyAssemblyError("Error replacing operand", asm_op)
