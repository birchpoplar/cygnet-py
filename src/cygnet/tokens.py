from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass

# Token type definitions

class TokenType(Enum):
    IDENTIFIER = auto()
    CONSTANT = auto()
    #Keywords
    INT = auto()
    VOID = auto()
    RETURN = auto()
    # Punctuation
    PAREN_OPEN = auto()
    PAREN_CLOSE = auto()
    BRACE_OPEN = auto()
    BRACE_CLOSE = auto()
    SEMICOLON = auto()
    # Structural
    NULL = auto()
    EOF = auto()
    
KEYWORDS = {
    "int": TokenType.INT,
    "void": TokenType.VOID,
    "return": TokenType.RETURN,
    }

PATTERNS = [
    (r'\s+', None),
    (r'//.*', None),
    (r'[a-zA-Z_]\w*\b', TokenType.IDENTIFIER),
    (r'[0-9]+\b', TokenType.CONSTANT),
    (r'\(', TokenType.PAREN_OPEN),
    (r'\)', TokenType.PAREN_CLOSE),
    (r'{', TokenType.BRACE_OPEN),
    (r'}', TokenType.BRACE_CLOSE),
    (r';', TokenType.SEMICOLON),
]

@dataclass
class Token:
    type: TokenType
    value: Optional[str] = None
    line_num: int = 0
