from typing import Any
from enum import Enum

Value = Any
Position = int | tuple[int, int]


class TokenType(Enum):
    LBRACK    = "("
    RBRACK    = ")"
    LSBRACK   = "{"
    RSBRACK   = "}"
    SQRLBRACK = "["
    SQRRBRACK = "]"
    MINUS     = "-"
    MULT      = "*"
    PLUS      = "+"
    SLASH     = "/"
    EQL       = "="
    ECM       = "!"
    QM        = "?"
    DOT       = "."
    SPACE     = " "
    DQUOTE    = '"'
    USCORE    = "_"
    DDOT      = ":"
    COMA      = ","
    GT        = ">"
    LT        = "<"
    DAC       = ";"

    NUMBER    = "number"
    FLOAT     = "float"
    LETTERS   = "letters"
    ILL       = "illegal"
    WS        = "whitespace"
    EOF       = "eof"


TOKEN_TABLE = {
    "(": TokenType.LBRACK,
    ")": TokenType.RBRACK,
    "{": TokenType.LSBRACK,
    "}": TokenType.RSBRACK,
    "[": TokenType.SQRLBRACK,
    "]": TokenType.SQRRBRACK,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    "/": TokenType.SLASH,
    "*": TokenType.MULT,
    "=": TokenType.EQL,
    "!": TokenType.ECM,
    "?": TokenType.QM,
    ".": TokenType.DOT,
    " ": TokenType.SPACE,
    '"': TokenType.DQUOTE,
    "_": TokenType.USCORE,
    ":": TokenType.DDOT,
    ",": TokenType.COMA,
    "<": TokenType.LT,
    ">": TokenType.GT,
    ";": TokenType.DAC,
    "eof": TokenType.EOF,
    "letters": TokenType.LETTERS,
    "number": TokenType.NUMBER,
    "float": TokenType.FLOAT,
    "illegal": TokenType.ILL,
    "whitespace": TokenType.WS,
}


class Token:
    def __init__(
        self,
        token_type: TokenType,
        value: Value,
        position: Position
    ) -> None:
        self.token_type = token_type
        self.value = value
        self.pos = position

    def __str__(self):
        return f"Token<type={self.token_type.name};value='{self.value}';position{self.pos}>"

    def __repr__(self):
        return f"Token<type={self.token_type.name};value='{self.value}';position{self.pos}>"
