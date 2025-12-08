from enum import Enum, auto
from dataclasses import dataclass
from os import CLONE_FILES
from typing import Optional
from pathlib import Path
import re

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

KEYWORDS = {
    "int": TokenType.INT,
    "void": TokenType.VOID,
    "return": TokenType.RETURN,
    }
    
@dataclass
class Token:
    type: TokenType
    value: Optional[str] = None
    
def read_lines(path: Path):
    with open(path, 'r') as f:
        lines = f.readlines()

    stripped_lines = [line.strip() for line in lines]

    return stripped_lines
    
def lexer(path: Path):
    lines = read_lines(path)
    print_lines(lines)

    for line in lines:
        for char in line:
            print(char)
        break

    patterns = [
        (r'[a-zA-Z_]\w*\b', TokenType.IDENTIFIER),
        (r'[0-9]+\b', TokenType.CONSTANT),
        (r'\(', TokenType.PAREN_OPEN),
        (r'\)', TokenType.PAREN_CLOSE),
        (r'{', TokenType.BRACE_OPEN),
        (r'}', TokenType.BRACE_CLOSE),
        ]

    for line in lines:
        pos = 0
        matches = []

        for pattern, token_type in patterns:
            match = re.match(pattern, line[pos:])
            if match:
                matches.append((match.group(), token_type, len(match.group())))

            if matches:
                longest = max(matches, key=lambda x: x[2])
                token_text, token_type, length = longest

            pos = pos + length
            print(token_text)
        
    
def print_lines(lines):

    max_num_width = len(str(len(lines)))
    line_num = 1
    
    for line in lines:
        print(f"{line_num:>{max_num_width}}: {line}")
        line_num += 1
        
