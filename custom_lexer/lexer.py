from collections import deque
from io import IOBase

from constants import DIGITS, KEYWORDS, LETTER_DIGITS, LETTERS
from custom_token import Token
from tokens import tt_tokens


class Lexer:
    def __init__(self) -> None:
        self.peek = None  # preparing peek char
        self.tokens = deque()  # preparing arr for tokens

    def __del__(self) -> None:
        del self.tokens
        del self.peek
        self.input = None

    def next(self) -> None:
        self.peek = self.input.read(1)

    def make_tokens(self, inp: IOBase) -> deque:  # noqa: C901, PLR0912, PLR0915
        self.input = inp
        self.next()
        while self.peek != "":  # when we get eof peek will look like ''
            # So, we just get char and compare it with all possible options,
            # then we call functions that will make token for this character(s)
            if self.peek in DIGITS:
                self.tokens.append(self.make_number())
            elif self.peek == "#":
                self.skip_comment()
            elif self.peek in LETTERS:
                self.tokens.append(self.make_id())
            elif self.peek == '"':
                self.tokens.append(self.make_string())
            elif self.peek == "!":
                self.tokens.append(self.make_not_equals())
            elif self.peek == "=":
                self.tokens.append(self.make_equals())
            elif self.peek == ">":
                self.tokens.append(self.make_greater_than())
            elif self.peek == "<":
                self.tokens.append(self.make_less_than())
            else:
                if self.peek.isspace():
                    pass
                elif self.peek == "%":
                    self.tokens.append(Token(tt_tokens.TT_MOD))
                elif self.peek == "+":
                    self.tokens.append(Token(tt_tokens.TT_PLUS))
                elif self.peek == "[":
                    self.tokens.append(Token(tt_tokens.TT_LSQUARE))
                elif self.peek == "]":
                    self.tokens.append(Token(tt_tokens.TT_RSQUARE))
                elif self.peek in ";\n":
                    self.tokens.append(Token(tt_tokens.TT_NEWLINE))
                elif self.peek == "-":
                    self.tokens.append(Token(tt_tokens.TT_MINUS))
                elif self.peek == "*":
                    self.tokens.append(Token(tt_tokens.TT_MUL))
                elif self.peek == ",":
                    self.tokens.append(Token(tt_tokens.TT_COMMA))
                elif self.peek == "/":
                    self.tokens.append(Token(tt_tokens.TT_DIV))
                elif self.peek == "(":
                    self.tokens.append(Token(tt_tokens.TT_LPAREN))
                elif self.peek == ")":
                    self.tokens.append(Token(tt_tokens.TT_RPAREN))
                elif self.peek == "{":
                    self.tokens.append(Token(tt_tokens.TT_LBRACKET))
                elif self.peek == "}":
                    self.tokens.append(Token(tt_tokens.TT_RBRACKET))
                elif self.peek == "&":
                    self.tokens.append(Token(tt_tokens.TT_KEY_AND))
                elif self.peek == "|":
                    self.tokens.append(Token(tt_tokens.TT_KEY_OR))
                else:
                    return f"Unknown character: {self.peek}"
                self.next()
        self.tokens.append(Token(tt_tokens.TT_EOF))
        return self.tokens

    # fun for creating identifier or keyword
    def make_id(self) -> Token:
        id_str = ""
        while self.peek != "" and self.peek in LETTER_DIGITS + "_":
            id_str += self.peek
            self.next()
        tok_type = tt_tokens.TT_KEYWORD if id_str in KEYWORDS else tt_tokens.TT_ID
        return Token(tok_type, id_str)

    def skip_comment(self) -> None:
        self.next()
        if self.peek == "#":
            """  # - oneline comm
                ## - multiline comm
            """
            while True:
                self.next()
                if self.peek == "#":
                    self.next()
                    if self.peek == "#":
                        self.next()
                        break

        else:
            while self.peek != "\n":
                self.next()

    def make_number(self) -> Token:
        num_str = ""
        dot_count = 0
        """
        all things that are related to variables are stupid as heck
        """
        while self.peek is not None and self.peek in DIGITS + ".":
            if self.peek == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.peek
            self.next()
        if dot_count == 0:
            return Token(tt_tokens.TT_INT, int(num_str))
        return Token(tt_tokens.TT_FLOAT, float(num_str))

    def make_string(self) -> Token:
        string = ""
        flag = False
        self.next()
        while self.peek is not None and self.peek != '"':
            string += self.peek
            self.next()
            if self.peek == '"':
                flag = True
        if flag:
            self.next()
            return Token(tt_tokens.TT_STRING, string)
        raise Exception('Expected " symbol')

    def make_equals(self) -> Token:
        tok_type = tt_tokens.TT_EQ
        self.next()
        if self.peek == "=":
            self.next()
            tok_type = tt_tokens.TT_BOOL_EQ
        return Token(tok_type)

    def make_not_equals(self) -> Token:
        tok_type = tt_tokens.TT_BOOL_NOT
        self.next()
        if self.peek == "=":
            self.next()
            tok_type = tt_tokens.TT_BOOL_NE
        return Token(tok_type)

    def make_less_than(self) -> Token:
        tok_type = tt_tokens.TT_BOOL_LT
        self.next()
        if self.peek == "=":
            self.next()
            tok_type = tt_tokens.TT_BOOL_LTE
        return Token(tok_type)

    def make_greater_than(self) -> Token:
        tok_type = tt_tokens.TT_BOOL_GT
        self.next()
        if self.peek == "=":
            self.next()
            tok_type = tt_tokens.TT_BOOL_GTE
        return Token(tok_type)
