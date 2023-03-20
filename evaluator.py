from ast_node import *

nil = LispList()
t = LispAtom('t')


def quote(operands: list, env: dict):
    if len(operands) != 1:
        raise Exception('quote only have one operand.')
    return operands[0]


def atom(operands: list, env: dict):
    if len(operands) != 1:
        raise Exception('atom only have one operand.')
    return t if Evaluator.eval(operands[0], env).is_atom() else nil


def eq(operands: list, env: dict):
    if len(operands) != 2:
        raise Exception('eq only have two operands.')
    x = Evaluator.eval(operands[0], env)
    y = Evaluator.eval(operands[1], env)

    if not x.is_atom() or not y.is_atom():
        return nil

    if isinstance(x, LispList) and isinstance(y, LispList):
        return t
    if isinstance(x, LispString) and isinstance(y, LispString):
        return t if x == y else nil
    if isinstance(x, LispNumber) and isinstance(y, LispNumber):
        return t if x.number == y.number else nil
    if isinstance(x, LispAtom) and isinstance(y, LispAtom):
        return t if x.literal == y.literal else nil
    return nil


def car(operands: list, env: dict):
    if len(operands) != 1:
        raise Exception('car only have one operand')
    x = Evaluator.eval(operands[0], env)
    if x.is_atom():
        if isinstance(x, LispList):
            return nil
        raise Exception('car require operand is a list')
    return x[0]


def cdr(operands: list, env: dict):
    if len(operands) != 1:
        raise Exception('cdr only have one operand')
    x = Evaluator.eval(operands[0], env)
    if x.is_atom():
        if isinstance(x, LispList):
            return nil
        raise Exception('cdr require operand is a list')
    return LispList(x[1:])


def cons(operands: list, env: dict):
    if len(operands) != 2:
        raise Exception('cons only have two operand')
    x = Evaluator.eval(operands[0], env)
    y = Evaluator.eval(operands[1], env)
    if not isinstance(y, LispList):
        raise Exception('value of y must be a list')
    new_list = LispList([x])
    new_list.extend(y)
    return new_list


def cond(operands: list, env: dict):
    for cond_tuple in operands:
        if not isinstance(cond_tuple, LispList) and len(cond_tuple) != 2:
            raise Exception('each element of cond must a tuple in form like (p e)')
        if Evaluator.eval(cond_tuple[0], env) == t:
            return Evaluator.eval(cond_tuple[1], env)
    return nil


base_operator = {
    'quote': quote,
    'atom': atom,
    'eq': eq,
    'car': car,
    'cdr': cdr,
    'cons': cons,
    'cond': cond
}


class Evaluator:
    @staticmethod
    def eval(root: LispElement, env: dict) -> LispElement:
        if root.is_atom():
            if isinstance(root, (LispNumber, LispString, LispList)):
                return root
            return env[root.literal]
        elif isinstance(root, LispList):
            head = root[0]
            tail = root[1:]
            if isinstance(head, LispAtom) and head.literal in base_operator:
                return base_operator[head.literal](tail, env)

            args = map(Evaluator.eval, tail)
            # func = Evaluator.eval(head, env)
            # if not isinstance(func, LispAtom):
            #     raise Exception('Error Header is not atom literal')
            #
            # # TODO: finish func(args)
