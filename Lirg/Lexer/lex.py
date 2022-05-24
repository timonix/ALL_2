import json


def file_to_list(file):
    f = open(file, "r")
    codeList = code_to_list(f.read())
    f.close()
    return codeList


def code_to_list(cc):
    for i in range(1, 10):
        cc = cc.lstrip(",")
        cc = cc.replace(" to ", ">to>")
        cc = cc.replace("\t", "")
        cc = cc.replace(" ", "")
        cc = cc.replace("{", "[")
        cc = cc.replace("}", "]")
        cc = cc.replace("\n", ",")
        cc = cc.replace("[,", "[")
        cc = cc.replace(",]", "]")
        cc = cc.replace(",,", ",")
        cc = cc.replace(")[", "),[")

    cc = cc.replace(",", "\",\"")
    cc = cc.replace(":[", "\":[\"")
    cc = cc.replace("\"[", "[\"")
    cc = cc.replace("]", "\"]")
    for i in range(10):
        cc = cc.replace("]\"]", "]]")

    cc = "[\"" + cc + "]"
    y = json.loads(cc)
    return y
