# Errors and Exceptions

class CompilerError(Exception):
    pass

class LexerError(CompilerError):
    def __init__(self, char, line_num, pos):
        self.char = char
        self.line_num = line_num
        self.pos = pos
        super().__init__(f"Lexer error: unexpected character '{char}' at line {line_num} position {pos}")
