from evaluator import Evaluator
from parser import Parser

if __name__ == '__main__':
    print("""Welcome to PyLisp REPL v0.0.1""")
    env = {}
    while True:
        source_code = input('> ')
        try:
            root = Parser(source_code).parse()
            result = Evaluator.eval(root, env)
            if result is not None:
                print(result)
        except Exception as e:
            print(f'{type(e).__name__}:\n\t{e}')
