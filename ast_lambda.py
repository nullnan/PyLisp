from ast_node import LispElement, LispList, LispAtom, LispNumber, LispString
import evaluator
from errors import EvalException


class LispLambda(LispElement):
    def __init__(self, parameters: LispList, body: LispElement, func_name: str = None):
        self.body = body
        self.parameters: list[str] = []
        self.func_name = func_name
        for parameter in parameters:
            if not isinstance(parameter, LispAtom) or isinstance(parameter, (LispNumber, LispString)):
                raise EvalException('lambda parameter must be a literal atom')
            self.parameters.append(parameter.literal)

    def is_atom(self):
        return False

    def get_func_name_or_id(self):
        return id(self) if self.func_name is None else self.func_name

    def __str__(self):
        return f'(λ {" ".join(self.parameters)})'

    def __repr__(self):
        return f'procedure#{self.get_func_name_or_id()} {str(self)}'

    def __eq__(self, other):
        return False

    def invoke(self, env: dict, args: list[LispElement]) -> LispElement:
        if len(self.parameters) != len(args):
            raise EvalException(f'{str(self)} require {len(self.parameters)} parameter but got {len(args)}')

        arguments = {}
        for index in range(len(self.parameters)):
            arguments[self.parameters[index]] = args[index]
        func_env = dict(env)
        func_env.update(arguments)

        return evaluator.Evaluator.eval(self.body, func_env)
