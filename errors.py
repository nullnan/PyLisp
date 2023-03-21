class MismatchParenthesesException(Exception):
    def __init__(self):
        super().__init__("Parentheses not match")


class NumberFormatException(Exception):
    def __init__(self, literal):
        super().__init__(f"The string of {repr(literal)} is not valid number.")
