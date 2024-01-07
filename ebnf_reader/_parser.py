from ._lexer import Lexer
from ._tokenizer import Token, TokenType


class SourceParser:
    def __init__(self, source_code: str) -> None:
        self.lex = Lexer(source_code)
        self.current_token: Token = next(self.lex)

    def _parse_token(self, token_type: TokenType):
        def iftok():
            self.current_token = next(self.lex)
            if self.current_token.token_type == TokenType.EOF:
                self.lex.step_back()
                raise ValueError(f"EOF: {self.current_token}; {self.lex.current_c}")
            if self.current_token.token_type == token_type:
                return self.current_token
            self.lex.step_back()
            raise ValueError(
                f"Expected {token_type}:{token_type.value}, got {self.current_token}"
            )

        return iftok

    def _parse_word(self, word: str):
        def wrd():
            self.current_token = next(self.lex)
            if self.current_token.token_type == TokenType.EOF:
                self.lex.step_back()
                raise ValueError(f"EOF: {self.current_token}; {self.lex.current_c}")
            if self.current_token.value == word:
                return self.current_token
            self.lex.step_back()
            raise ValueError(f"Exptected: {word}, got: {self.current_token}")

        return wrd

    def _or(self, *parsers):
        def if_or():
            for parser in parsers:
                try:
                    expr = parser()
                    return expr
                except:  # noqa:722
                    continue
            raise ValueError("No matching expressions")

        return if_or

    def _concat(self, *parsers):
        def if_all():
            parsed = []
            for parser in parsers:
                expr = parser()
                parsed.append(expr)
            if len(parsed) == 1:
                return parsed[0]
            return tuple(parsed)

        return if_all

    def _none_or_one(self, parser):
        def just_parse():
            try:
                expr = parser()
                return expr
            except:  # noqa:722
                return ()

        return just_parse

    def _none_or_more(self, parser):
        def while_parsed():
            exprs = []
            while True:
                try:
                    expr = parser()
                    exprs.append(expr)
                except:  # noqa:722
                    break
            if len(exprs) == 1:
                return exprs[0]
            return tuple(exprs)

        return while_parsed
