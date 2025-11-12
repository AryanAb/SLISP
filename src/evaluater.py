from typing import Union
from lisp_parser import parse
import math
import os

constants = {}
variables = {}
functions = {}


def import_module(children):
    assert len(children) == 1
    path = children[0][1:-1]
    script_path = os.path.realpath(__file__)
    lib_path = f"{script_path}/../../stdlib/{path}"
    if os.path.isfile(lib_path):
        execute(lib_path)
    else:
        execute(path)


def evaulate_simple_math(operation, operands, scope) -> float:
    assert len(operands) == 2
    operand0, operand1 = evaluate(operands[0], scope), evaluate(operands[1], scope)
    assert (isinstance(operand0, float) or isinstance(operand0, int)) and (
        isinstance(operand1, float) or isinstance(operand1, int)
    )
    if operation == "+":
        return operand0 + operand1
    elif operation == "-":
        return operand0 - operand1
    elif operation == "*":
        return operand0 * operand1
    elif operation == "/":
        return operand0 / operand1
    else:
        return operand0 % operand1


def evaluate_math_comparison(operation, operands, scope):
    assert len(operands) == 2
    operand0, operand1 = evaluate(operands[0], scope), evaluate(operands[1], scope)
    assert (isinstance(operand0, float) or isinstance(operand0, int)) and (
        isinstance(operand1, float) or isinstance(operand1, int)
    )
    if operation == ">":
        return operand0 > operand1
    elif operation == "<":
        return operand0 < operand1
    elif operation == ">=":
        return operand0 >= operand1
    elif operation == "<=":
        return operand0 <= operand1
    elif operation == "!=":
        return operand0 != operand1
    else:
        return operand0 == operand1


def evaluate_define_constant(args, scope):
    assert len(args) == 2
    name, value = args
    constants[name] = evaluate(value, scope)


def evaluate_define_variable(args, scope):
    assert len(args) == 2
    name, value = args
    variables[name] = evaluate(value, scope)


def evaluate_mutate(args, scope):
    assert len(args) == 2
    name, value = args
    if name in constants:
        raise TypeError
    if name in variables:
        variables[name] = evaluate(value, scope)
    else:
        raise NameError


def define_function(children):
    assert len(children) == 3
    func_name, params, body = children
    functions[func_name] = (params, body)


def define_lambda(children):
    assert len(children) == 2
    params, body = children
    return (params, body)


def evaluate_function(func_name, args, scope):
    params, body = functions[func_name]
    assert len(params) == len(args)
    new_scope = {param: evaluate(arg, scope) for param, arg in zip(params, args)}
    return evaluate(body, scope | new_scope)


def evaluate_lambda(lambda_func, args, scope):
    params, body = define_lambda(lambda_func)
    assert len(params) == len(args)
    new_scope = {param: evaluate(arg, scope) for param, arg in zip(params, args)}
    return evaluate(body, scope | new_scope)


def evaluate_if_statement(children, scope):
    assert len(children) == 3
    condition = evaluate(children[0], scope)
    if condition:
        return evaluate(children[1], scope)
    return evaluate(children[2], scope)

def evaluate_cond_statement(children, scope):
    for child in children:
        condition, action = child
        if (evaluate(condition, scope)):
            return evaluate(action, scope)

def evaluate_for_statement(children, scope):
    lst = evaluate(children[1], scope)
    assert isinstance(lst, list)
    new_scope = scope.copy()
    for elem in lst:
        new_scope[children[0]] = elem
        evaluate(children[2], new_scope)


def evaluate_list(elements, scope):
    lst = []
    for element in elements:
        lst.append(evaluate(element, scope))
    return lst


def evaluate_build_list(children, scope):
    length = evaluate(children[0], scope)
    assert isinstance(length, int)
    return [evaluate(children[1], scope)] * length


def evaluate_list_ref(children, scope):
    lst = evaluate(children[0], scope)
    assert isinstance(lst, list)
    index = evaluate(children[1], scope)
    assert isinstance(index, int)
    return lst[index]


def evaluate_in_range(children, scope):
    assert len(children) >= 1
    start, end, step = 0, 0, 1
    if len(children) == 1:
        end = evaluate(children[0], scope)
    elif len(children) == 2 or len(children) == 3:
        start = evaluate(children[0], scope)
        end = evaluate(children[1], scope)
    if len(children) == 3:
        step = evaluate(children[2], scope)
    return [i for i in range(start, end, step)]


def evaluate_fold(children, scope):
    lst = evaluate(children[0], scope)
    assert isinstance(lst, list)
    func = children[1]
    acc = evaluate(children[2], scope)
    for elem in lst:
        acc = evaluate([func, elem, acc], scope)
    return acc


def evaluate_map(children, scope):
    lst = evaluate(children[0], scope)
    assert isinstance(lst, list)
    func = children[1]
    new_lst = []
    for elem in lst:
        new_lst.append(evaluate([func, elem], scope))
    return new_lst


def evaluate_atomic(atom: str, scope) -> Union[float, str]:
    if atom == "True":
        return True
    elif atom == "False":
        return False
    elif isinstance(atom, float) or isinstance(atom, int):
        return atom
    elif atom.replace(".", "", 1).isdigit():
        return float(atom) if "." in atom else int(atom)
    elif atom[0] == '"' and atom[-1] == '"':
        return f"{atom}"
    elif atom in scope:
        return scope[atom]
    elif atom in constants:
        return constants[atom]
    elif atom in variables:
        return variables[atom]
    raise NameError


def evaluate(tree, scope):
    if not isinstance(tree, list):
        return evaluate_atomic(tree, scope)
    else:
        parent, children = tree[0], tree[1:]
        if parent in ["+", "-", "*", "/", "%"]:
            return evaulate_simple_math(parent, children, scope)
        elif parent in [">", "<", ">=", "<=", "=", "!="]:
            return evaluate_math_comparison(parent, children, scope)
        elif parent == 'floor':
            value = evaluate(children[0], scope)
            assert isinstance(value, float) or isinstance(value, int)
            return math.floor(value)
        elif parent == "import":
            import_module(children)
        elif parent == "const":
            evaluate_define_constant(children, scope)
        elif parent == "let":
            evaluate_define_variable(children, scope)
        elif parent == "mutate":
            evaluate_mutate(children, scope)
        elif parent == "defunc":
            define_function(children)
        elif parent == "lambda":
            define_lambda(children)
        elif parent == "if":
            return evaluate_if_statement(children, scope)
        elif parent == "cond":
            return evaluate_cond_statement(children, scope)
        elif parent == "for":
            evaluate_for_statement(children, scope)
        elif parent == "list":
            return evaluate_list(children, scope)
        elif parent == "build-list":
            return evaluate_build_list(children, scope)
        elif parent == "list-ref":
            return evaluate_list_ref(children, scope)
        elif parent == "in-range":
            return evaluate_in_range(children, scope)
        elif parent == "fold":
            return evaluate_fold(children, scope)
        elif parent == "map":
            return evaluate_map(children, scope)
        elif parent == "print":
            value = evaluate(children[0], scope)
            if isinstance(value, str):
                print(value[1:-1])
            else:
                print(value)
        elif isinstance(parent, list) and parent[0] == "lambda":
            return evaluate_lambda(parent[1:], children, scope)
        elif parent in functions:
            return evaluate_function(parent, children, scope)
        else:
            raise TypeError

"""
Below are functions required to open a file and interpret it.
They are in this file to avoid circular imports.
"""

def get_s_expressions(code):
    s_expressions = []

    stack = []
    s_expression = ""
    char_idx = 0
    while char_idx < len(code):
        char = code[char_idx]
        if char == "(":
            stack.append(char)
        elif char == ")":
            stack.pop()
        s_expression += char
        if not stack and s_expression:
            s_expressions.append(s_expression)
            s_expression = ""
        char_idx += 1

    return filter(lambda s_expression: s_expression != "\n", s_expressions)


def execute(file_path):
    with open(file_path) as file:
        non_comment_lines = filter(lambda line: not line.startswith(';'), file.readlines())
        s_expressions = get_s_expressions(''.join(non_comment_lines))
        for s_expression in s_expressions:
            tree = parse(s_expression)
            res = evaluate(tree, {})
            if res is not None:
                print(res)
