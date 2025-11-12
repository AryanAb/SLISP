from lisp_parser import parse
from evaluater import evaluate

REPL_INFO = "SLSIP v0.1.0"

def get_input():
    print(REPL_INFO)
    while True:
        code = input(">>> ")
        tree = parse(code)
        res = evaluate(tree, {})
        if res is not None:
            print(res)
