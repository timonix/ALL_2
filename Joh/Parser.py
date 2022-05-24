import copy


def get_arguments(function):
    if function[3]["type"] == "keyword_void":
        return []

    pass


def parseType(type, secondary):
    if type == "keyword_int" and secondary == "single_index":
        return "integer_array"
    if type == "keyword_int":
        return "integer"


def token_in_list(token_type, list_of_tokens):
    for token in list_of_tokens:
        if token["type"] == token_type:
            return True
    return False


def token_sequence_in_list(sequence, list_of_tokens):
    for i, j in zip(sequence, list_of_tokens[0:len(sequence)]):
        if j["type"] != i:
            return False
    return True


def get_locals(function, global_variables):
    locals_variables = {}
    code = []
    for s in function:
        define_array_sequence_with_initial = ["define", "variable", "set", "keyword_int", "single_index", "set_initial",
                                              "array_index"]
        define_array_sequence = ["define", "variable", "set", "keyword_int", "single_index"]
        define_integer_sequence_with_initial = ["define", "variable", "set", "keyword_int", "set_initial", "integer"]
        define_integer_sequence = ["define", "variable", "set", "keyword_int"]
        define_for_variables = ['keyword_for', '(', 'variable', ':', 'variable', ')', '{']

        if token_sequence_in_list(define_array_sequence_with_initial, s):
            locals_variables[s[1]["name"]] = {"type": "integer_array",
                                              "length": s[4]["value"],
                                              "initial": {'type': 'integer_array', 'value': s[6]["indices"]}}
        elif token_sequence_in_list(define_array_sequence, s):
            locals_variables[s[1]["name"]] = {"type": "integer_array",
                                              "length": s[4]["value"]}
        elif token_sequence_in_list(define_integer_sequence_with_initial, s):
            locals_variables[s[1]["name"]] = {"type": "integer",
                                              "initial": s[5]}
        elif token_sequence_in_list(define_integer_sequence, s):
            locals_variables[s[1]["name"]] = {"type": "integer"}

        elif token_sequence_in_list(define_for_variables, s):
            if s[4]["name"] in locals_variables:
                if locals_variables[s[4]["name"]]["type"] == "integer_array":
                    locals_variables[s[2]["name"]] = {"type": "integer"}
                    locals_variables[s[2]["name"]+".index"] = {"type": "index"}
            code.append(s)
        else:
            code.append(s)

    return code, locals_variables


def split_by_line(function):
    lines = []
    line = []
    for token in function:

        if token["type"] == "newLine":
            lines.append(copy.copy(line))
            line.clear()
        else:
            line.append(token)
    return lines


def parseCodeLine(line):
    if line[0]["type"] == "keyword_return":
        return {"return": {"argument": line[1]}}

    pass


def parse_for_loop(code):

    print(code)
    pass


def parse_code(code):

    return_sequence = ["keyword_return"]
    for_sequence = ["keyword_for"]

    if token_sequence_in_list(return_sequence, code[0]):
        return code[1:], [{"return": {"argument": code[0][1]}}]
    if token_sequence_in_list(for_sequence, code[0]):
        return parse_for_loop(code)

    return code, []


def get_code(function):
    parsed_code = []
    code = function

    for i in range(10):
        code, parsed = parse_code(code)
        parsed_code.extend(parsed)
        if len(code) == 0:
            return parsed

    return []


def extract_single_global(i, code):
    name = code[i + 1]["name"]
    type = parseType(code[i + 3]["type"])
    if code[i + 4]["type"] == "set_initial":
        initial_value = code[i + 5]
        return {"name": name, "type": type, "initial_value": initial_value}
    return {"name": name, "type": type}


def extract_globals(code, stop):
    globals = {}

    for i in range(stop):
        if code[i]["type"] == "define" and code[i + 1]["type"] == "variable":
            globals[code[i + 1]["name"]] = extract_single_global(i, code)

    return globals


def get_first_function_start(code):
    for i in range(len(code) - 1):
        if code[i]["type"] == "define" and code[i + 1]["type"] == "function":
            return i;


def removeHeader(code_lines):
    return code_lines[1:]


def parse(code):
    parsed_code = {}
    raw_functions = extract_functions(code)
    first_function_start = get_first_function_start(code)
    parsed_code["global_variables"] = extract_globals(code, first_function_start)

    for fun in raw_functions.items():
        args = get_arguments(fun[1])
        parsed_code["functions"] = {fun[0]: {"arguments": args}}
        code_lines = split_by_line(fun[1])
        code_lines = removeHeader(code_lines)
        code_lines, parsed_code["functions"][fun[0]]["local_variables"] = get_locals(code_lines, parsed_code["global_variables"])
        parsed_code["functions"][fun[0]]["code"] = get_code(code_lines)

    return parsed_code


def extract_single_function(i, code):
    fun_code = []
    started = False
    paran_count = 0

    while True:

        if started and paran_count == 0:
            return fun_code
        if code[i]["type"] == "{":
            started = True
            paran_count = paran_count + 1
        if code[i]["type"] == "}":
            started = True
            paran_count = paran_count - 1

        fun_code.append(code[i])
        i += 1


def extract_functions(code):
    functions = {}

    for i in range(len(code) - 1):
        if code[i]["type"] == "define" and code[i + 1]["type"] == "function":
            functions[code[i + 1]["name"]] = extract_single_function(i, code)

    return functions
