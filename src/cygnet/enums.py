from enum import IntEnum, Enum

SUCCESS = 0
FAIL = 1

class CompilerReturnCode(IntEnum):
    COMPILE_SUCCESS = 0
    PREPROCESS_ERROR = 1
    COMPILE_ERROR = 2

class AnsiColors(Enum):
    GREEN = '\033[92m'
    RESET = '\033[0m'
        
