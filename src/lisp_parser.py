def is_atomic(code: str) -> bool:
    return code[0] != '(' and code[-1] != ')'

def is_s_expression(code: str) -> bool:
    return code[0] == '(' and code[-1] == ')'

def parse(code: str):
    if len(code) == 0:
        return []
    
    if is_atomic(code):
        return code
    if is_s_expression(code):
        char_idx = 1
        elements = []
        arg = ''
        stack = []
        while char_idx < len(code) - 1:
            char = code[char_idx]
            if (arg == '' and char == ' ') or char == '\n' or char == '\t':
                pass
            elif char != ' ':
                arg += char
                if char == '(':
                    stack.append('(')
                elif char == ')':
                    stack.pop()
                elif char == '"':
                    if stack and stack[-1] == '"':
                        stack.pop()
                    else:
                        stack.append('"')
            elif char == ' ' and arg != '':
                if not stack:
                    elements.append(parse(arg))
                    arg = ''
                else:
                    arg += char
            char_idx += 1
        if stack:
            raise SyntaxError
        if arg == "":
            elements.append([])
        else:
            elements.append(parse(arg))

        return elements