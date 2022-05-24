import json
import re

def make_string_code_into_list(string_code, log_level = False):
    string_code = string_code.replace("){", ")\n{")
    string_code = string_code.rstrip("\n")
    rows = string_code.split("\n")
    string_code = ""
    for r in rows:
        if "{" in r:
            string_code += r + "\n"
        elif "}" in r:
            string_code += r + "\n"
        elif len(r)<=1:
            pass
        else:
            string_code += "\""+r+"\"\n"
    string_code = string_code.replace(" to ", ">to>")
    string_code = string_code.replace(" ", "")
    string_code = string_code.replace("\t", "")
    log(log_level, string_code)
    string_code = string_code.replace("\n", "")
    log(log_level, string_code)
    string_code = string_code.replace("{", ",[")
    string_code = string_code.replace("}", "]")
    string_code = string_code.replace("]\"", "],\"")
    log(log_level, string_code)
    string_code = string_code.replace("\"\"", "\",\"")
    string_code = "[" + string_code + "]"


    log(log_level, string_code)

    return json.loads(string_code)


def log(level, msg):
    if level == True:
        print(msg)
