# Errors and Exceptions

from cygnet.tokens import TokenType, Token


class CompilerError(Exception):
    pass

class LexerError(CompilerError):
    def __init__(self, char, line_num, pos):
        self.char = char
        self.line_num = line_num
        self.pos = pos
        super().__init__(f"Lexer error: unexpected character '{char}' at line {line_num} position {pos}")


class ParserError(CompilerError):
    def __init__(self, message, line=None, token=Token(TokenType.NULL, None, 0)):
        self.message = message
        self.line = line
        self.token = token
        super().__init__(f"Parser error: {message}, '{token.value}' at line {line}")


class CodeGenError(CompilerError):
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        super().__init__(f"Code generator error: {message}, '{node}")
