import re


def getName(globals):
    temp = re.findall(r'\w*', globals)
    return temp[0]


def getNumberOfArgs(globals):
    temp = re.findall(r'\d+', globals)
    if len(temp) == 0:
        return 0
    return int(temp[0])


def getType(globals):
    if globals[-1].isdigit():
        return "i"
    else:
        return globals[-1]


def getValueAsString(globals):  # TODO

    temp = re.findall(r'[\d.]*', globals)
    temp = [x for x in temp if x]

    if getType(globals) == "F":  # float array
        return temp
    if getType(globals) == "I":  # Integer Array
        return temp
    if getType(globals) == "D":  # Double Array
        return temp
    if getType(globals) == "L":  # Long Array
        return temp

    return temp[0]


class Extractor:
    global_dict = {}
    function_dict = {}

    def extract_globals(self, code_tree):
        last_fun = None
        for globals_scoped_instances in code_tree:
            if type(globals_scoped_instances) is not list:
                if ")" in globals_scoped_instances:

                    self.function_dict[getName(globals_scoped_instances)] = {
                        "args": getNumberOfArgs(globals_scoped_instances)}
                    last_fun = getName(globals_scoped_instances)
                else:
                    self.global_dict[getName(globals_scoped_instances)] = {"type": getType(globals_scoped_instances),
                                                                           "value": getValueAsString(
                                                                               globals_scoped_instances)}
            else:
                self.function_dict[last_fun]["code"] = globals_scoped_instances
