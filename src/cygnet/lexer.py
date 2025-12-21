from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List
from .print import print_token_list, print_error, print_msg
from .errors import LexerError
from .tokens import TokenType, KEYWORDS, PATTERNS, Token
import re


class Lexer():
    def __init__(self, source_code: List[str]):
        self.source_code = source_code
        self.tokens = []
        self.token_type = ""
        self.line_num = 1
        self.in_comment = False

    def lex(self):
        
        for line in self.source_code:
            pos = 0

            while pos < len(line):

                matches = []

                if not self.in_comment:
                    comment_start_match = re.match(r'/\*', line[pos:])
                    if comment_start_match:
                        self.in_comment = True
                        pos += comment_start_match.end()
                        continue

                if self.in_comment:
                    comment_end_match = re.match(r'\*/', line[pos:])
                    if comment_end_match:
                        self.in_comment = False
                        pos += comment_end_match.end()
                        continue
                    else:
                        pos += 1
                        continue

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
                        self.tokens.append(Token(type=token_type, value=value, line_num=self.line_num))

                else:
                    raise LexerError(line[pos], self.line_num, pos)

            self.line_num += 1

        self.tokens.append(Token(type=TokenType.EOF, value=None, line_num=self.line_num))
        
        return self.tokens

def lexer(source_code: List[str], print_tokens: bool = False):

    tokens = []
    token_type = ""
    line_num = 1
    in_comment = False
    
    for line in source_code:
        pos = 0

        while pos < len(line):

            matches = []

            if not in_comment:
                comment_start_match = re.match(r'/\*', line[pos:])
                if comment_start_match:
                    in_comment = True
                    pos += comment_start_match.end()
                    continue

            if in_comment:
                comment_end_match = re.match(r'\*/', line[pos:])
                if comment_end_match:
                    in_comment = False
                    pos += comment_end_match.end()
                    continue
                else:
                    pos += 1
                    continue
            
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
