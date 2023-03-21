from ast_lambda import LispLambda
from ast_node import *
from base_operator import base_operators
from errors import *


class Evaluator:
    @staticmethod
    def eval(root: LispElement, env: dict) -> LispElement:
        if root.is_atom():
            if isinstance(root, (LispNumber, LispString, LispList)):
                return root
            assert isinstance(root, LispAtom)

            try:
                value = env[root.literal]
            except KeyError as e:
                raise UnboundedNameException(root.literal) from e

            if not value.is_atom() and isinstance(value, LispList) and isinstance(value[0], LispAtom) \
                    and value[0].literal == 'lambda':
                return Evaluator.eval(value, env)
            else:
                return value
        elif isinstance(root, LispList):
            head = root[0]
            tail = root[1:]
            if isinstance(head, LispAtom) and head.literal in base_operators:
                return base_operators[head.literal](tail, env)

            args = list(map(lambda elem: Evaluator.eval(elem, env), tail))
            func = Evaluator.eval(head, env)
            if isinstance(func, LispAtom):
                if isinstance(func, (LispNumber, LispString)):
                    raise EvalException(f'{str(func)} is not a procedure')
                try:
                    func = env[func.literal]
                except KeyError as e:
                    raise UnboundedNameException(func.literal) from e
            if not isinstance(func, LispLambda):
                raise EvalException(f'{str(func)} is not a procedure')

            return func.invoke(env, args)
