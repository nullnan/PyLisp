class MismatchParenthesesException(Exception):
    def __init__(self):
        super().__init__("Parentheses not match")


class NumberFormatException(Exception):
    def __init__(self, literal: str):
        super().__init__(f"The string of {repr(literal)} is not valid number.")


class UnboundedNameException(Exception):
    def __init__(self, name: str):
        super().__init__(f'The name {repr(name)} is not defined yet.')


class EvalException(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)


class BuiltinFunctionException(EvalException):
    pass
