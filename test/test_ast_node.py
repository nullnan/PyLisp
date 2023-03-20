import unittest
from ast_node import *


class TestAstNode(unittest.TestCase):
    def test_atom(self):
        self.assertEqual(True, LispAtom('+').is_atom())

    def test_number(self):
        self.assertEqual(True, LispNumber('1234', -1234).is_atom())

    def test_string(self):
        self.assertEqual(True, LispString('Test').is_atom())

    def test_list(self):
        self.assertEqual(True, LispList().is_atom())
        self.assertEqual(True, LispList([]).is_atom())
        self.assertEqual(False, LispList([1, 2, 3]).is_atom())


if __name__ == '__main__':
    unittest.main()
