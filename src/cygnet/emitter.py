from .errors import TackyAssemblyError
from .codegen import Program, Ret, Mov, Imm, Register, AllocateStack, Unary, UnaryOperator, Neg, Not, Stack, Reg


class Emitter:
    def __init__(self, code_root: Program):
        self.code_root = code_root
        self.assembly_lines = []
        self.indent = 4

    def emit_program(self, program):
        self.emit_function(program.function)
        self.assembly_lines.append("# Confirm code does not require executable stack")
        self.assembly_lines.append(".section .note.GNU-stack,\"\",@progbits")
        
    def emit_function(self, function):
        indentation = " "*self.indent 
        # self.assembly_lines.append(self._emit_comment("Function", function))
        self.assembly_lines.append(f"{indentation}.globl {function.name}")
        self.assembly_lines.append(f"{function.name}:")
        self._emit_insn("pushq", "%rbp")
        self._emit_insn("movq", "%rsp", "%rbp")
        for instruction in function.instructions:
            self.emit_instruction(instruction)

    def emit_instruction(self, instruction):
        if isinstance(instruction, Ret):
            self._emit_insn("movq", "%rbp", "%rsp")
            self._emit_insn("popq", "%rbp")
            self._emit_insn("ret")
        elif isinstance(instruction, Mov):
            self._emit_insn("movl", instruction.op_src, instruction.op_dst)
        elif isinstance(instruction, Unary):
            if isinstance(instruction.unary_op, Neg):
                self._emit_insn("negl", instruction.operand)
            elif isinstance(instruction.unary_op, Not):
                self._emit_insn("notl", instruction.operand)
        elif isinstance(instruction, AllocateStack):
            # Note here the stack value stored as negative value, need to use abs() given subq
            self._emit_insn("subq", f"${abs(instruction.value)}", "%rsp")

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
        # self.assembly_lines.append(self._emit_comment("Instruction", formatted_ops))
        self.assembly_lines.append(line)

    def _format_operand(self, operand):
        if isinstance(operand, str):
            return operand
        elif isinstance(operand, Imm):
            return f"${operand.value}"
        elif isinstance(operand, Register):
            return self._format_register(operand.reg)
        elif isinstance(operand, Stack):
            return f"{operand.offset}(%rbp)"
        raise TackyAssemblyError(f"Unexpected operand type", operand)

    def _format_register(self, register):
        if register == Reg.AX:
            return f"%eax"
        elif register == Reg.R10:
            return f"%r10d"
        raise TackyAssemblyError(f"Unexpected register type", register)
