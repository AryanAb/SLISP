from lisp_parser import parse
from evaluate import evaluate

REPL_INFO = "REPLIS v0.1.0"

def get_input():
    print(REPL_INFO)
    while True:
        code = input(">>> ")
        tree = parse(code)
        print(tree)
        res = evaluate(tree, {})
        if res is not None:
            print(res)
