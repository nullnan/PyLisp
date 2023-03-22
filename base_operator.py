from ast_lambda import LispLambda
from ast_node import LispList, LispAtom, LispString, LispNumber, LispElement
import evaluator
from errors import BuiltinFunctionException

nil = LispList()
t = LispAtom('t')


def quote(operands: list, env: dict):
    if len(operands) != 1:
        raise BuiltinFunctionException('quote only have one operand')
    return operands[0]


def atom(operands: list, env: dict):
    if len(operands) != 1:
        raise BuiltinFunctionException('atom only have one operand')
    return t if evaluator.Evaluator.eval(operands[0], env).is_atom() else nil


def eq(operands: list, env: dict):
    if len(operands) != 2:
        raise BuiltinFunctionException('eq only have two operands')
    x = evaluator.Evaluator.eval(operands[0], env)
    y = evaluator.Evaluator.eval(operands[1], env)

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
        raise BuiltinFunctionException('car only have one operand')
    x = evaluator.Evaluator.eval(operands[0], env)
    if x.is_atom():
        if isinstance(x, LispList):
            return nil
        raise BuiltinFunctionException('car require operand is a list')
    assert isinstance(x, LispList)
    return x[0]


def cdr(operands: list, env: dict):
    if len(operands) != 1:
        raise BuiltinFunctionException('cdr only have one operand')
    x = evaluator.Evaluator.eval(operands[0], env)
    if x.is_atom():
        if isinstance(x, LispList):
            return nil
        raise BuiltinFunctionException('cdr require operand is a list')
    return LispList(x[1:])


def cons(operands: list, env: dict):
    if len(operands) != 2:
        raise BuiltinFunctionException('cons only have two operand')
    x = evaluator.Evaluator.eval(operands[0], env)
    y = evaluator.Evaluator.eval(operands[1], env)
    if not isinstance(y, LispList):
        raise BuiltinFunctionException(f'value of {str(y)} must be a list')
    new_list = LispList([x])
    new_list.extend(y)
    return new_list


def cond(operands: list, env: dict):
    for cond_tuple in operands:
        if not isinstance(cond_tuple, LispList) and len(cond_tuple) != 2:
            raise BuiltinFunctionException('each element of cond must a tuple in form like (p e)')
        if evaluator.Evaluator.eval(cond_tuple[0], env) == t:
            return evaluator.Evaluator.eval(cond_tuple[1], env)
    return nil


def mk_fun(operands: list, env: dict):
    if len(operands) != 2:
        raise BuiltinFunctionException('lambda require a parameters\' list and an expression body')
    if not isinstance(operands[0], LispList):
        raise BuiltinFunctionException('parameter must be a list')
    return LispLambda(operands[0], operands[1])


def define_fun(operands: list, env: dict):
    if len(operands) != 3:
        raise BuiltinFunctionException('defun require a procedure name, a parameters\' list and an expression body')
    func_name: LispElement = operands[0]
    parameters = operands[1]
    func_body = operands[2]
    if not func_name.is_atom() or isinstance(func_name, (LispNumber, LispString, LispList)):
        raise BuiltinFunctionException(
            'procedure name need be a atom and not a string either a number or an empty list'
        )
    assert isinstance(func_name, LispAtom)
    if not isinstance(parameters, LispList):
        raise BuiltinFunctionException('procedure parameter must provided in a list')
    assert isinstance(parameters, LispList)
    func = LispLambda(parameters, func_body, func_name.literal)
    env[func_name.literal] = func
    return None


def plus(operands: list, env: dict):
    result_sum = 0
    for operand in operands:
        number = evaluator.Evaluator.eval(operand, env)
        if not isinstance(number, LispNumber):
            raise BuiltinFunctionException(f'{operand} is not a number')
        assert isinstance(number, LispNumber)
        result_sum += number.number
    return LispNumber(result_sum)


def minus(operands: list, env: dict):
    result_sum = 0
    for operand in operands:
        number = evaluator.Evaluator.eval(operand, env)
        if not isinstance(number, LispNumber):
            raise BuiltinFunctionException(f'{operand} is not a number')
        assert isinstance(number, LispNumber)
        result_sum -= number.number
    return LispNumber(result_sum)


def mul(operands: list, env: dict):
    result_sum = 1
    for operand in operands:
        number = evaluator.Evaluator.eval(operand, env)
        if not isinstance(number, LispNumber):
            raise BuiltinFunctionException(f'{operand} is not a number')
        assert isinstance(number, LispNumber)
        result_sum *= number.number
    return LispNumber(result_sum)


base_operators = {
    'quote': quote,
    'atom': atom,
    'eq': eq,
    'car': car,
    'cdr': cdr,
    'cons': cons,
    'cond': cond,
    'lambda': mk_fun,
    'defun': define_fun,
    '+': plus,
    '-': minus,
    '*': mul
}
