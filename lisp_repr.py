from evaluator import Evaluator
from parser import Parser

if __name__ == '__main__':
    print("""
Welcome to PyLisp REPL v0.0.1
    """)
    env = {}
    while True:
        source_code = input('> ')
        root = Parser(source_code).parse()
        result = Evaluator.eval(root, env)
        print(str(result))
