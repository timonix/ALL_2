import re

func_pattern = (r"\w+(?=\()", "FUNCTION", True)
var_pattern = (r"\w+", "VARIABLE", True)

patterns = [func_pattern,
            var_pattern,
            (r"\(", "L_PARENTHESIS", False),
            (r"\)", "R_PARENTHESIS", False),
            (r"\{", "L_braces", False),
            (r"\}", "R_braces", False),
            (r"\n", "LINE", False),
            (r" +", "SPACE", False),
            (r"=", "SET", False),
            (r"[+*-]", "OPERATION", True),
            (r"==", "TEST_EQUAL", False),
            (r"\t", "TAB", False)
            ]


def best_match(matches):
    best_id = 0
    best_span = 0
    for idx, m in enumerate(matches):

        if m[0].span()[1] > best_span:
            best_span = m[0].span()[1]
            best_id = idx

    return matches[best_id]


def make_string_code_into_list(code_string):
    code = code_string
    output = []

    while (len(code) > 0):
        matching = []
        for p in patterns:
            if re.match(p[0], code):
                matching.append((re.match(p[0], code), p))
        if len(matching) == 0:

            return remove_filler(output)
        best = (best_match(matching))
        if best[1][2]:  # is a name
            output.append((best[1][1], code[:best[0].span()[1]]))
        else:
            output.append(best[1][1])
        code = code[best[0].span()[1]:]

    return remove_filler(output)

def remove_filler(code):
    no_filler_code = []
    for c in code:
        if c != "SPACE":
            no_filler_code.append(c)

    return no_filler_code

def keywords(code):
    c = code

    for c in code:


