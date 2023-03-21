import unittest

from errors import *
from parser import Parser
from ast_node import *


class TestParseAtom(unittest.TestCase):
    def test_None(self):
        p = Parser(None)
        root = p.parse()
        self.assertEqual(None, root)

    def test_empty_seq(self):
        p = Parser('')
        root = p.parse()
        self.assertEqual(None, root)

    def test_atom(self):
        p = Parser('foo')
        root = p.parse()
        self.assertEqual(LispAtom('foo'), root)

        p = Parser('你好')
        root = p.parse()
        self.assertEqual(LispAtom('你好'), root)

        p = Parser('\\this')
        root = p.parse()
        self.assertEqual(LispAtom('\\this'), root)

        p = Parser('🥵')
        root = p.parse()
        self.assertEqual(LispAtom('🥵'), root)

        p = Parser('😅😅')  # emoji atom should be allowed
        root = p.parse()
        self.assertEqual(LispAtom('😅😅'), root)

        p = Parser('()')  # Empty list is atom value
        root = p.parse()
        self.assertEqual(LispList([]), root)

        p = Parser('-')
        root = p.parse()
        self.assertEqual(root, LispAtom('-'))

        p = Parser('+')
        root = p.parse()
        self.assertEqual(root, LispAtom('+'))

        p = Parser('/')
        root = p.parse()
        self.assertEqual(root, LispAtom('/'))

        p = Parser('*')
        root = p.parse()
        self.assertEqual(root, LispAtom('*'))

    def test_atom_number(self):
        p = Parser('1234')
        root = p.parse()
        self.assertEqual(LispNumber('1234', 1234), root)

        p = Parser('-1234')
        root = p.parse()
        self.assertEqual(LispNumber('-1234', -1234), root)

        p = Parser('0')
        root = p.parse()
        self.assertEqual(LispNumber('0', -0), root)

    def test_atom_string(self):
        p = Parser('"abcdef"')
        root = p.parse()
        self.assertEqual(LispString('abcdef'), root)

        p = Parser('"\\"\\""')
        root = p.parse()
        self.assertEqual(LispString('""'), root)

        p = Parser('"\\u4f60\\u597d"')
        root = p.parse()
        self.assertEqual(LispString('你好'), root)


class TestParseList(unittest.TestCase):
    def test_parse_list(self):
        foo_root = LispList([LispAtom('foo')])

        p = Parser('(foo)')
        root = p.parse()
        self.assertEqual(foo_root, root)

        p = Parser('( foo )')
        root = p.parse()
        self.assertEqual(foo_root, root)

    def test_parse_list_multi(self):
        foo_bar_root = LispList([LispAtom('foo'), LispAtom('bar')])

        p = Parser('(foo bar)')
        root = p.parse()
        self.assertEqual(foo_bar_root, root)

        p = Parser('( foo   bar  )')
        root = p.parse()
        self.assertEqual(foo_bar_root, root)

    def test_parse_list_nested(self):
        a_b_nc_d = LispList([LispAtom('a'), LispAtom('b'), LispList([LispAtom('c')]), LispAtom('d')])

        p = Parser('(a b (c) d)')
        root = p.parse()
        self.assertEqual(a_b_nc_d, root)

        p = Parser('( a   b (c) d  )')
        root = p.parse()
        self.assertEqual(a_b_nc_d, root)

    def test_parse_quote(self):
        p = Parser('\'x')
        root = p.parse()
        self.assertEqual(LispList([LispAtom('quote'), LispAtom('x')]), root)

        p = Parser('\'()')
        root = p.parse()
        self.assertEqual(LispList([LispAtom('quote'), LispList()]), root)

        p = Parser('\'\'x')
        root = p.parse()
        self.assertEqual(LispList([LispAtom('quote'), LispList([LispAtom('quote'), LispAtom('x')])]), root)

        p = Parser('(a \'(a b) b)')
        root = p.parse()
        self.assertEqual(LispList(
            [LispAtom('a'), LispList([LispAtom('quote'), LispList([LispAtom('a'), LispAtom('b')])]), LispAtom('b')]),
            root)


def assert_roundtrip(testcase, code: str):
    root = Parser(code).parse()
    testcase.assertEqual(code, str(root))


class TestRoundTrip(unittest.TestCase):
    def test_roundtrip(self):
        assert_roundtrip(self, '(quote (a b c))')

        assert_roundtrip(self, '(atom (atom (quote a)))')


class TestParseError(unittest.TestCase):
    def test_parse_bracket_not_complete(self):
        with self.assertRaises(MismatchParenthesesException):
            Parser('(').parse()
            Parser(')').parse()
            Parser('(((()))').parse()

    def test_number_format(self):
        with self.assertRaises(NumberFormatException):
            Parser('-1223sad21').parse()
            Parser('123abc21').parse()
            Parser('123.1231').parse()


if __name__ == '__main__':
    unittest.main()
