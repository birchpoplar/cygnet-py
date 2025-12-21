from dataclasses import dataclass
from .tokens import TokenType, Token
from typing import List
from .errors import ParserError

# AST Nodes, abstract base classes

@dataclass
class ASTNode:
    line: int

    def __str__(self):
        return f"Line {self.line}"


@dataclass
class Statement(ASTNode):

    def __str__(self):
        return f"Statement at {self.line}"
    

@dataclass
class Exp(ASTNode):

    def __str__(self):
        return f"Exp at {self.line}"

    
@dataclass
class Function(ASTNode):
    name: str
    body: Statement

    def __str__(self):
        return f"Function({self.name}, {self.body}) at {self.line}"


@dataclass
class Program(ASTNode):
    function: 'Function'

    def __str__(self):
        return f"Program {self.function.name} at {self.line}"
    
    
# Derived node classes
    
@dataclass
class Return(Statement):
    expr: Exp

    def __str__(self):
        return f"Return({self.expr}) at {self.line}"

    
@dataclass
class Constant(Exp):
    value: int

    def __str__(self):
        return f"Constant({self.value}) at {self.line}"


# Main parsing class
    
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    # Helper functions

    def get_line(self):
        if self.current >= len(self.tokens):
            raise ParserError(f"Beyond end of tokens list, position {self.current}, tokens length {len(self.tokens)}")
        return self.tokens[self.current].line_num
    
    def peek(self):
        if self.current >= len(self.tokens):
            raise ParserError(f"Beyond end of tokens list, position {self.current}, tokens length {len(self.tokens)}")
        return self.tokens[self.current]
    
    def consume(self):
        token = self.peek()
        self.current += 1
        return token
        
    def expect(self, expected_type):
        actual = self.peek()
        if actual.type == expected_type:
            return self.consume()
        elif actual.type == TokenType.EOF:
            raise ParserError(f"Unexpected EOF token, expected {expected_type}", actual.line_num, actual)
        else:
            raise ParserError(f"Expected {expected_type}", actual.line_num, actual)
    
    # Parsing functions
    def parse_exp(self):
        value_token = self.expect(TokenType.CONSTANT)
        return Constant(self.get_line(), value_token.value)
        
    
    def parse_statement(self):
        self.expect(TokenType.RETURN)
        expr = self.parse_exp()
        self.expect(TokenType.SEMICOLON)
        return Return(self.get_line(), expr)

    
    def parse_function(self):
        self.expect(TokenType.INT)
        id_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.PAREN_OPEN)
        self.expect(TokenType.VOID)
        self.expect(TokenType.PAREN_CLOSE)
        self.expect(TokenType.BRACE_OPEN)
        statement = self.parse_statement()
        self.expect(TokenType.BRACE_CLOSE)
        return Function(self.get_line(), id_token.value, statement)
                    
    
    def parse_program(self):
        function_token = self.parse_function()
        self.expect(TokenType.EOF)
        return Program(function_token.line, function_token)

    
    # Main 
    def parse(self):
        return self.parse_program()
    

def print_ast_out(node, indent = 0):
    prefix = "-" * indent

    if isinstance(node, Program):
        print(f"{prefix}Program, ln {node.line}")
        print_ast_out(node.function, indent + 1)
        
    elif isinstance(node, Function):
        print(f"{prefix}Function({node.name}), ln {node.line}")
        print_ast_out(node.body, indent + 1)
        
    elif isinstance(node, Return):
        print(f"{prefix}Return, ln {node.line}")
        print_ast_out(node.expr, indent + 1)
        
    elif isinstance(node, Constant):
        print(f"{prefix}Constant({node.value}), ln {node.line}")

    else:
        print("No node match")
