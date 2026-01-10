from dataclasses import dataclass
from typing import List
from .parser import ASTNode, Return as ASTReturn, Constant as ASTConstant, Unary as ASTUnary, Complement as ASTComplement, Negate as ASTNegate
from .errors import TackyGenError

# Tacky Generation nodes, abstract base classes

@dataclass
class TackyGenNode:
    pass


@dataclass
class UnaryOp(TackyGenNode):
    pass


@dataclass
class Val(TackyGenNode):
    pass


@dataclass
class Instruction(TackyGenNode):
    pass


@dataclass
class Function(TackyGenNode):
    identifier: str
    body: List[Instruction]


@dataclass
class Program(TackyGenNode):
    function: 'Function'


# Derived node classes

@dataclass
class Return(Instruction):
    val: Val


@dataclass
class Unary(Instruction):
    unary_op: UnaryOp
    src: Val
    dst: Val

    
@dataclass
class Constant(Val):
    value: int


@dataclass
class Var(Val):
    identifier: str

    
@dataclass
class Complement(UnaryOp):
    pass


@dataclass
class Negate(UnaryOp):
    pass

# Tacky generator

class TackyGenerator:
    def __init__(self, ast_root: ASTNode):
        self.ast_root = ast_root
        self.temp_ctr = 0

    # Code generation functions
    def generate(self):
        return self.generate_program(self.ast_root)
        
    def generate_program(self, ast_program):
        function = self.generate_function(ast_program.function)
        return Program(function=function)

    def generate_function(self, ast_function):
        body = self.generate_statement(ast_function.body)
        return Function(ast_function.name, body)

    def generate_statement(self, ast_statement):
        instructions = []
        if isinstance(ast_statement, ASTReturn):
            val, exp_instructions = self.generate_exp(ast_statement.expr)
            instructions.extend(exp_instructions)
            instructions.append(Return(val))
            return instructions

    def generate_exp(self, ast_exp):
        match ast_exp:
            case ASTConstant():
                return (Constant(ast_exp.value), [])
            case ASTUnary():
                src_val, src_instructions = self.generate_exp(ast_exp.expr)
                dst = self._make_temp()
                tacky_op = self._convert_unop(ast_exp.unary_op)
                instruction = Unary(tacky_op, src_val, dst)
                return (dst, src_instructions + [instruction])
                
    def _make_temp(self):
        name = f"tmp.{self.temp_ctr}" 
        self.temp_ctr += 1
        return Var(name)


    def _convert_unop(self, unary_op):
        match unary_op:
            case ASTComplement():
                return Complement()
            case ASTNegate():
                return Negate()

def print_tacky(node, indent = 0):
    prefix = "_" * indent

    match node:
        case Program():
            print(f"{prefix}Program")
            print_tacky(node.function, indent+1)
        case Function():
            print(f"{prefix}Function {node.identifier}")
            for instruction in node.body:
                print_tacky(instruction, indent+1)
        case Return():
            print(f"{prefix}Return")
            print_tacky(node.val, indent+1)
        case Unary():
            print(f"{prefix}Unary {node.unary_op}")
            print(f"{prefix}src: ")
            print_tacky(node.src, indent+1)
            print(f"{prefix}dst: ")
            print_tacky(node.dst, indent+1)
        case Constant():
            print(f"{prefix}Constant {node.value}")
        case Var():
            print(f"{prefix}Var {node.identifier}")
        case _:
            print("TBD")
            
