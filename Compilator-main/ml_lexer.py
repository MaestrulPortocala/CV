
import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
   
    INT_TYPE    = auto()
    FLOAT_TYPE  = auto()
    BOOL_TYPE   = auto()
    INT_LITERAL   = auto()
    FLOAT_LITERAL = auto()
    BOOL_LITERAL  = auto()
    IDENTIFIER = auto()
    IF         = auto()
    ELSE       = auto()
    WHILE      = auto()
    PRINT      = auto()
    PLUS    = auto()
    MINUS   = auto()
    STAR    = auto()
    SLASH   = auto()
    PERCENT = auto()
    EQ     = auto()  
    NEQ    = auto()  
    LT     = auto()  
    GT     = auto()   
    LTE    = auto()  
    GTE    = auto()  
    AND = auto()  
    OR  = auto()   
    NOT = auto()   
    ASSIGN = auto()  
    LPAREN    = auto()  
    RPAREN    = auto()  
    LBRACE    = auto()  
    RBRACE    = auto() 
    SEMICOLON = auto()  
    COMMA     = auto()  
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.col})"


class LexerError(Exception):
    def __init__(self, msg: str, line: int, col: int):
        super().__init__(f"[Eroare Lexicala] Linia {line}, Coloana {col}: {msg}")
        self.line = line
        self.col  = col


KEYWORDS = {
    "if":    TokenType.IF,
    "else":  TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "int":   TokenType.INT_TYPE,
    "float": TokenType.FLOAT_TYPE,
    "bool":  TokenType.BOOL_TYPE,
    "true":  TokenType.BOOL_LITERAL,
    "false": TokenType.BOOL_LITERAL,
}
TOKEN_RULES: List[tuple] = [
    (TokenType.FLOAT_LITERAL, re.compile(r'\d+\.\d+')),
    (TokenType.INT_LITERAL,   re.compile(r'\d+')),
    (TokenType.EQ,            re.compile(r'==')),
    (TokenType.NEQ,           re.compile(r'!=')),
    (TokenType.LTE,           re.compile(r'<=')),
    (TokenType.GTE,           re.compile(r'>=')),
    (TokenType.AND,           re.compile(r'&&')),
    (TokenType.OR,            re.compile(r'\|\|')),
    (TokenType.LT,            re.compile(r'<')),
    (TokenType.GT,            re.compile(r'>')),
    (TokenType.NOT,           re.compile(r'!')),
    (TokenType.PLUS,          re.compile(r'\+')),
    (TokenType.MINUS,         re.compile(r'-')),
    (TokenType.STAR,          re.compile(r'\*')),
    (TokenType.SLASH,         re.compile(r'/')),
    (TokenType.PERCENT,       re.compile(r'%')),
    (TokenType.ASSIGN,        re.compile(r'=')),
    (TokenType.LPAREN,        re.compile(r'\(')),
    (TokenType.RPAREN,        re.compile(r'\)')),
    (TokenType.LBRACE,        re.compile(r'\{')),
    (TokenType.RBRACE,        re.compile(r'\}')),
    (TokenType.SEMICOLON,     re.compile(r';')),
    (TokenType.COMMA,         re.compile(r',')),
    (TokenType.IDENTIFIER,    re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')),
]

WHITESPACE = re.compile(r'[ \t\r\n]+')
COMMENT    = re.compile(r'(#|//)[^\n]*')  


class Lexer:

    def __init__(self, source: str):
        self.source = source
        self.pos    = 0
        self.line   = 1
        self.col    = 1
        self.tokens: List[Token] = []

    def _advance(self, n: int):
        for ch in self.source[self.pos: self.pos + n]:
            if ch == '\n':
                self.line += 1
                self.col   = 1
            else:
                self.col += 1
        self.pos += n

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
           
            m = WHITESPACE.match(self.source, self.pos)
            if m:
                self._advance(m.end() - self.pos)
                continue

          
            m = COMMENT.match(self.source, self.pos)
            if m:
                self._advance(m.end() - self.pos)
                continue

            matched = False
            for tok_type, pattern in TOKEN_RULES:
                m = pattern.match(self.source, self.pos)
                if m:
                    value = m.group(0)
                   
                    if tok_type == TokenType.IDENTIFIER and value in KEYWORDS:
                        tok_type = KEYWORDS[value]
                    self.tokens.append(Token(tok_type, value, self.line, self.col))
                    self._advance(len(value))
                    matched = True
                    break

            if not matched:
                raise LexerError(
                    f"Caracter neașteptat: {self.source[self.pos]!r}",
                    self.line, self.col
                )

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
