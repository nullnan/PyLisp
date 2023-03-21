from ast_lambda import LispLambda
from ast_node import *
from base_operator import base_operators


class Evaluator:
    @staticmethod
    def eval(root: LispElement, env: dict) -> LispElement:
        if root.is_atom():
            if isinstance(root, (LispNumber, LispString, LispList)):
                return root
            assert isinstance(root, LispAtom)
            value = env[root.literal]
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

            args = list(map(lambda e: Evaluator.eval(e, env), tail))
            func = Evaluator.eval(head, env)
            if isinstance(func, LispAtom):
                if isinstance(func, (LispNumber, LispNumber)):
                    raise Exception(f'{str(func)} is not a procedure')
                func = env[func.literal]
            if not isinstance(func, LispLambda):
                raise Exception(f'{str(func)} is not a procedure')

            if len(func.parameters) != len(args):
                raise Exception(f'{str(func)} require {len(func.parameters)} parameter but got {len(args)}')

            return func.invoke(env, args)
