from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from .print import print_token_list, print_error, print_msg
from .errors import LexerError
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

PATTERNS = [
    (r'\s+', None),
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
    
def lexer(source_code: List[str], print_tokens: bool = False):

    # TODO: Add in comment token /* ... */, and also //
    
    tokens = []
    token_type = ""
    line_num = 1
    
    for line in source_code:
        pos = 0

        while pos < len(line):

            matches = []
            
            for pattern, token_type in PATTERNS:
                match = re.match(pattern, line[pos:])

                if match:
                    matches.append((token_type, match.group(), match.end(), match.span()))

            if matches:
                longest_match = max(matches, key=lambda x: x[2])
                token_type, value, length, span = longest_match
                pos = pos + span[1]

                if token_type == TokenType.IDENTIFIER:
                    for keyword, keyword_type in KEYWORDS.items():
                        if value == keyword:
                            token_type = keyword_type
                        
                if token_type:
                    tokens.append((token_type, value, line_num))

            else:
                raise LexerError(line[pos], line_num, pos)
                    
        line_num += 1
        
    if print_tokens:
        print_token_list(tokens)

    return 0
