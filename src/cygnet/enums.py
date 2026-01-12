from enum import IntEnum, Enum
from dataclasses import dataclass

SUCCESS = 0
FAIL = 1

class CompilerReturnCode(IntEnum):
    COMPILE_SUCCESS = 0
    PREPROCESS_ERROR = 1
    COMPILE_ERROR = 2

class AnsiColors(Enum):
    GREEN = '\033[92m'
    RESET = '\033[0m'

class CompileStage(Enum):
    LEX = 1
    PARSE = 2
    TACKY = 3
    CODEGEN = 4
    ASSEMBLE = 5
    LINK = 6

@dataclass
class PrintFlags:
    source: bool = False
    tokens: bool = False
    ast: bool = False
    tacky: bool = False
    ir: bool = False
    asm: bool = False
