from lisp_parser import parse
from evaluate import evaluate

def execute(file):
    with open(file) as f:
        tree = parse(f.read())
        evaluate(tree, {})