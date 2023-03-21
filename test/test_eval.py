import unittest

from ast_node import *
from evaluator import Evaluator
from parser import Parser


def assertLispOutput(testcase, expect_output: str, code: str, env=None):
    if env is None:
        env = {}
    expect_root = Parser(expect_output).parse()
    root = Evaluator.eval(Parser(code).parse(), env)
    testcase.assertEqual(expect_root, root)


class TestEval(unittest.TestCase):

    @staticmethod
    def eval_lisp(code, env=None):
        if env is None:
            env = {}
        root = Parser(code).parse()
        return Evaluator.eval(root, env)

    def test_eval_atom(self):
        self.assertEqual(LispNumber('12345', 12345), self.eval_lisp('12345'))

        self.assertEqual(LispString("Hello"), self.eval_lisp('\"Hello\"'))

        self.assertEqual(LispList([]), self.eval_lisp('()'))

        self.assertEqual(LispNumber('5', 5), self.eval_lisp("x", {'x': LispNumber('5', 5)}))

    def test_eval_quote(self):
        self.assertEqual(LispList([]), self.eval_lisp('(quote ())'))

        self.assertEqual(LispList([LispAtom('quote'), LispAtom('x')]), self.eval_lisp('(quote (quote x))'))

        self.assertEqual(LispAtom('a'), self.eval_lisp('(quote a)'))

        self.assertEqual(LispList([LispAtom('a'), LispAtom('b'), LispAtom('c')]), self.eval_lisp('(quote (a b c))'))

        self.assertEqual(LispList([]), self.eval_lisp('\'()'))

        self.assertEqual(LispAtom('a'), self.eval_lisp('\'a'))

        assertLispOutput(self, '()', '\'()')

    def test_eval_atom_operator(self):
        assertLispOutput(self, 't', '(atom \'a)')

        assertLispOutput(self, 't', '(atom \'())')

        assertLispOutput(self, '()', '(atom \'(a b c))')

        assertLispOutput(self, 't', '(atom (atom \'a))')

        assertLispOutput(self, '()', '(atom \'(atom \'a))')

    def test_eval_eq_operator(self):
        assertLispOutput(self, 't', '(eq \'a \'a)')

        assertLispOutput(self, '()', '(eq \'a \'b)')

        assertLispOutput(self, 't', '(eq \'() \'())')

        assertLispOutput(self, '()', '(eq \'(a) \'(b))')

    def test_eval_car_operator(self):
        assertLispOutput(self, 'a', '(car \'(a b c))')

        assertLispOutput(self, '(a b)', '(car \'((a b) c d))')

        assertLispOutput(self, '()', '(car \'())')

    def test_eval_cdr_operator(self):
        assertLispOutput(self, '(b c)', '(cdr \'(a b c))')

        assertLispOutput(self, '(c d)', '(cdr \'((a b) c d))')

        assertLispOutput(self, '()', '(cdr \'())')

    def test_eval_cons_operator(self):
        assertLispOutput(self, '(a b c)', '(cons \'a \'(b c))')

        assertLispOutput(self, '(a b c)', '(cons \'a (cons \'b (cons \'c \'())))')

        assertLispOutput(self, 'a', '(car (cons \'a \'(b c)))')

        assertLispOutput(self, '(b c)', '(cdr (cons \'a \'(b c)))')

    def test_eval_cond_operator(self):
        assertLispOutput(self, 'second', '(cond ((eq \'a \'b) \'first) ((atom \'a)  \'second))')

    def test_eval_lambda(self):
        assertLispOutput(self, 't', '((lambda () \'t))')

        assertLispOutput(self, 'a', '((lambda (x) (car x)) \'(a b c))')

        assertLispOutput(self, '(a b c)', '((lambda (f) (f \'(b c))) \'(lambda (x) (cons \'a x)))')

    def test_eval_defun(self):
        env = {}
        assertLispOutput(self, '', """
(defun subst (x y z)
  (cond ((atom z)
         (cond ((eq z y) x)
               ('t z)))
        ('t (cons (subst x y (car z))
                  (subst x y (cdr z))))))
        """, env)
        assertLispOutput(self, 'm', '(subst \'m \'b \'b)', env)

        assertLispOutput(self, '(m)', '(subst \'m \'b \'(b))', env)

        assertLispOutput(self, '(a m (a m c) d)', '(subst \'m \'b \'(a b (a b c) d))', env)
