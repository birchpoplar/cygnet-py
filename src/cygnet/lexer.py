from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from .print import print_token_list, print_error, print_msg
from .errors import LexerError
from .tokens import TokenType, KEYWORDS, PATTERNS, Token
import re

    
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
                    tokens.append(Token(type=token_type, value=value, line_num=line_num))

            else:
                raise LexerError(line[pos], line_num, pos)
                    
        line_num += 1

    tokens.append(Token(type=TokenType.EOF, value=None, line_num=line_num))
        
    if print_tokens:
        print_token_list(tokens)

    return tokens
