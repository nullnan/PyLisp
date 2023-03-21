import ast
import re
from ast_node import *
from errors import MismatchParenthesesException, NumberFormatException


class Parser:
    string_re = re.compile(r'(?<!\\)\"')
    atom_re = re.compile(r'\s|\)')
    number_re = re.compile(r'^-?\d+$')

    def __init__(self, s_exp: str | None):
        self.s_exp = s_exp
        self.parentheses_stack = 0

    def __repr__(self):
        return f'LispParser(source={repr(self.s_exp)})'

    def parse_atom(self) -> LispAtom:
        assert len(self.s_exp) > 0 and not self.s_exp[0].isspace()
        literal = re.split(Parser.atom_re, self.s_exp)[0]
        self.s_exp = self.s_exp[len(literal):]
        return LispAtom(literal)

    def parse_num(self) -> LispAtom | LispNumber:
        assert len(self.s_exp) > 0 and (self.s_exp[0].isdigit() or self.s_exp[0] == '-')
        if self.s_exp[0] == '-':
            if len(self.s_exp) <= 1 or not self.s_exp[1].isdigit():
                return self.parse_atom()
        literal_num = re.split(Parser.atom_re, self.s_exp)[0]
        if re.fullmatch(Parser.number_re, literal_num) is None:
            raise NumberFormatException(literal_num)
        num = int(literal_num)
        self.s_exp = self.s_exp[len(literal_num):]
        return LispNumber(num)

    def parse_list(self) -> LispList:
        assert len(self.s_exp) > 0 and self.s_exp[0] == '('
        self.s_exp = self.s_exp[1:]
        self.parentheses_stack += 1
        root = LispList()
        while self.s_exp:
            if self.s_exp[0] == ')':
                self.parentheses_stack -= 1
                self.s_exp = self.s_exp[1:]
                return root
            elif self.s_exp[0].isspace():
                self.s_exp = self.s_exp.lstrip()
            else:
                root.append(self.parse())
        return root

    def parse_string(self) -> LispString:
        assert len(self.s_exp) > 0 and self.s_exp[0] == '"'
        self.s_exp = self.s_exp[1:]
        end_quote = re.search(Parser.string_re, self.s_exp)
        unescaped_string = self.s_exp[:end_quote.start()]
        escaped_string = ast.literal_eval('\"' + unescaped_string + '\"')
        self.s_exp = self.s_exp[end_quote.end():]
        return LispString(escaped_string)

    def parse(self) -> LispElement | None:
        if self.s_exp is None:
            return None

        while self.s_exp:
            if self.s_exp[0].isdigit() or self.s_exp[0] == '-':
                return self.parse_num()
            elif self.s_exp[0] == '(':
                current_level = self.parentheses_stack
                root = self.parse_list()
                if self.parentheses_stack != current_level:
                    raise MismatchParenthesesException()
                return root
            elif self.s_exp[0] == '"':
                return self.parse_string()
            elif self.s_exp[0] == '\'':
                self.s_exp = self.s_exp[1:]
                return LispList([LispAtom('quote'), self.parse()])
            elif self.s_exp[0].isspace():
                self.s_exp = self.s_exp.lstrip()
            else:
                return self.parse_atom()
