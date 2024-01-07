from typing import Callable

from .tokenizer import TOKEN_TABLE, Token


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.current_c = 0
        self.tokens = []
        self._is_eof = False

        self._comment_char = ";"

    def __iter__(self):
        return self

    def step_back(self):
        self.current_c -= 1
        char = self.code[self.current_c]
        if char.isalpha():
            while char.isalpha():
                self.current_c -= 1
                char = self.code[self.current_c]
            self.current_c += 1
        elif char.isnumeric():
            while char.isnumeric():
                self.current_c -= 1
                char = self.code[self.current_c]
            self.current_c += 1

    def __next__(self) -> Token:
        if self._is_eof:
            raise StopIteration

        if self.current_c >= len(self.code):
            self._is_eof = True
            return Token(TOKEN_TABLE["eof"], "", self.current_c)

        char: str = self.code[self.current_c]
        if char in TOKEN_TABLE:
            if self.current_c + 1 < len(self.code):
                if (
                    char == self._comment_char
                    and 
                    self.code[self.current_c+1] == self._comment_char
                ):
                    return self._skip_if_predicate(lambda x: x != "\n")
            self.current_c += 1
            return Token(TOKEN_TABLE[char], char, self.current_c)
        elif char.isalpha():
            return self._build_literal(self.isalpha)
        elif char.isnumeric():
            return self._build_literal(self.isnumber)
        elif self.iswhitespace(char):
            return self._skip_if_predicate(self.iswhitespace)
        else:
            self.current_c += 1
            return Token(TOKEN_TABLE["illegal"], char, self.current_c)

    def _skip_if_predicate(self, predicate: Callable):
        try:
            while predicate(self.code[self.current_c]):
                self.current_c += 1
            return next(self)
        except IndexError:
            self._is_eof = True
            self.current_c -= 1
            return Token(TOKEN_TABLE["eof"], "", self.current_c)

    def _build_literal(self, predicate: Callable):
        literal = ""
        start_c = self.current_c

        while predicate(char := self.code[self.current_c]):
            literal += char
            self.current_c += 1

        tt = (
            TOKEN_TABLE["number"]
            if self.isnumber(self.code[self.current_c - 1])
            else TOKEN_TABLE["letters"]
        )

        return Token(tt, literal, (start_c, self.current_c))

    def isnumber(self, char: str):
        return char.isnumeric()

    def isalpha(self, char: str):
        return char.isalpha()

    def iswhitespace(self, char: str):
        return char in ["\n", "\t"]
