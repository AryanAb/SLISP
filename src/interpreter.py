from lisp_parser import parse
from evaluate import evaluate

def get_s_expressions(code):
    s_expressions = []

    stack = []
    s_expression = ''
    char_idx = 0
    while char_idx < len(code):
        char = code[char_idx]
        if char == '(':
            stack.append(char)
        elif char == ')':
            stack.pop()
        s_expression += char
        if not stack and s_expression:
            s_expressions.append(s_expression)
            s_expression = ''
        char_idx += 1
    
    return filter(lambda s_expression: s_expression != '\n', s_expressions)



def execute(file_path):
    with open(file_path) as file:
        s_expressions = get_s_expressions(file.read())
        for s_expression in s_expressions:
            tree = parse(s_expression)
            res = evaluate(tree, {})
            if res is not None:
                print(res)