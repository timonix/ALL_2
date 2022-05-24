import re
import copy

prio_4 = [{"regex": r"^\>> *", "type": "operation_shift_right"},
          {"regex": r"^\<< *", "type": "operation_shift_left"}]

prio_5 = [{"regex": r"^def +", "type": "define"},
          {"regex": r"^void *", "type": "keyword_void"},
          {"regex": r"^int *", "type": "keyword_int"},
          {"regex": r"^return *", "type": "keyword_return"},
          {"regex": r"^for *", "type": "keyword_for"},
          {"regex": r"^float *", "type": "keyword_float"},
          {"regex": r"^double *", "type": "keyword_double"},
          {"regex": r"^long *", "type": "keyword_long"},
          {"regex": r"^\n *", "type": "newLine"},
          {"regex": r"^\= *", "type": "set"},
          {"regex": r"^\:\= *", "type": "set_initial"},
          {"regex": r"^\( *", "type": "("},
          {"regex": r"^\+ *", "type": "operation_add"},
          {"regex": r"^\- *", "type": "operation_sub"},
          {"regex": r"^\* *", "type": "operation_mul"},
          {"regex": r"^\/ *", "type": "operation_div"},
          {"regex": r"^\> *", "type": "operation_greater"},
          {"regex": r"^\< *", "type": "operation_less"},
          {"regex": r"^xor +", "type": "operation_xor"},
          {"regex": r"^xnor +", "type": "operation_xnor"},
          {"regex": r"^or +", "type": "operation_or"},
          {"regex": r"^nor +", "type": "operation_nor"},
          {"regex": r"^and +", "type": "operation_and"},
          {"regex": r"^nand +", "type": "operation_nand"},
          {"regex": r"^not +", "type": "operation_nand"},
          {"regex": r"^\) *", "type": ")"},
          {"regex": r"^\{ *", "type": "{"},
          {"regex": r"^\} *", "type": "}"}]

prio_6 = [
    {"regex": r"^\: *", "type": ":"},
    {"regex": r"^\D\w* *(?=\()", "type": "function", "name": ""},
    {"regex": r"^\[\d+\] *", "type": "single_index", "value": ""},
    {"regex": r"^\[[\d+,]+\] *", "type": "array_index", "indices": []},
    {"regex": r"^\[\d+\.\.\d+\] *", "type": "array_index", "indices": []},
    {"regex": r"^\D\w*\.index *", "type": "index", "name": ""}
]

prio_7 = [
    {"regex": r"^\D\w* *", "type": "variable", "name": ""},
    {"regex": r"^\d+L *", "type": "long", "value": ""},
    {"regex": r"^\d+\.\d+D *", "type": "double", "float": ""}
]

prio_8 = [
    {"regex": r"^\d+ *", "type": "integer", "value": ""},
    {"regex": r"^\d+\.\d+ *", "type": "float", "float": ""}
]


def lex(string_code):
    lexed = []
    local_code = string_code
    for i in range(80):

        if p5 := match(local_code, prio_5):
            lexed.append(p5[0])
            local_code = p5[1]

        elif p6 := match(local_code, prio_6):
            lexed.append(p6[0])
            local_code = p6[1]

        elif p7 := match(local_code, prio_7):
            lexed.append(p7[0])
            local_code = p7[1]

        elif p7 := match(local_code, prio_8):
            lexed.append(p7[0])
            local_code = p7[1]

    for l in lexed:
        l.pop("regex", None)
    return lexed


def match(string_code, prio):
    for pattern in prio:
        p = copy.deepcopy(pattern)
        m = re.findall(p["regex"], string_code)
        if len(m) == 1:
            if "name" in p:
                p["name"] = m[0].replace(" ", "")
            if "value" in p:
                p["value"] = int(m[0]
                                 .replace(" ", "")
                                 .replace("[", "")
                                 .replace("]", ""))
            if "float" in p:
                p["float"] = float(m[0].replace(" ", ""))

            if "indices" in p:
                if ".." in m[0]:
                    r = m[0].replace(" ", "").replace("[", "").replace("]", "").split("..")
                    p["indices"] = [*range(int(r[0]), int(r[1])+1, 1)]
                else:
                    p["indices"] = eval(m[0].replace(" ", ""))

            return p, string_code[len(m[0]):]
