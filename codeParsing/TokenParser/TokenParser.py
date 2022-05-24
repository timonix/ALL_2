# Takes lists of tokens from lexer and parses into tree

class Pattern:

    def match(self, input_list):
        for idx, element in enumerate(self.pattern):
            if len(input_list) < len(self):
                return False
            if isinstance(input_list[idx], tuple):
                if element != input_list[idx][0]:
                    return False
            else:
                if element != input_list[idx]:
                    return False
        return True

    def __init__(self, list_of_types):
        self.pattern = list_of_types

    def __len__(self):
        return len(self.pattern)


variable_Pattern_0 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", "NUMBER", "R_INDEXING"]),
                      "type": "VARIABLE_INDEXED",
                      "index_pos": 2,
                      "variable_pos": 0}
variable_Pattern_1 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", 'VARIABLE', "R_INDEXING"]),
                      "type": "VARIABLE_INDEXED",
                      "index_pos": 2,
                      "variable_pos": 0}
variable_Pattern_2 = {"PATTERN": Pattern(['VARIABLE']),
                      "type": "VARIABLE",
                      "variable_pos": 0}

array_Pattern_0 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", 'VARIABLE', "TO", 'VARIABLE', "R_INDEXING"]),
                   "type": "ARRAY",
                   "start_index_pos": 2,
                   "stop_index_pos": 4,
                   "variable_pos": 0}

array_Pattern_1 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", 'NUMBER', "TO", 'VARIABLE', "R_INDEXING"]),
                   "type": "ARRAY",
                   "start_index_pos": 2,
                   "stop_index_pos": 4,
                   "variable_pos": 0}

array_Pattern_2 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", 'VARIABLE', "TO", 'NUMBER', "R_INDEXING"]),
                   "type": "ARRAY",
                   "start_index_pos": 2,
                   "stop_index_pos": 4,
                   "variable_pos": 0}

array_Pattern_3 = {"PATTERN": Pattern(['VARIABLE', "L_INDEXING", 'NUMBER', "TO", 'NUMBER', "R_INDEXING"]),
                   "type": "ARRAY",
                   "start_index_pos": 2,
                   "stop_index_pos": 4,
                   "variable_pos": 0}

array_patterns = [array_Pattern_0, array_Pattern_1, array_Pattern_2, array_Pattern_3]

array_literal_start_pattern = {"PATTERN": Pattern(['L_ARROW']), "type": "ARRAY_LITERAL"}
array_literal_stop_pattern = {"PATTERN": Pattern(['R_ARROW']), "type": "ARRAY_LITERAL"}

set_Pattern = {"PATTERN": Pattern(['VAL_SET']), "type": "VAL_SET"}
line_Pattern = {"PATTERN": Pattern(['LINE']), "type": "LINE"}
l_bracket = {"PATTERN": Pattern(['L_BRACKET']), "type": "L_BRACKET"}
r_bracket = {"PATTERN": Pattern(['R_BRACKET']), "type": "R_BRACKET"}


return_pattern_0 = {"PATTERN": Pattern(['RETURN', 'NUMBER']),
                  "type": "RETURN",
                  "variable_pos": 0}

return_pattern_1 = {"PATTERN": Pattern(['RETURN', 'VARIABLE']),
                  "type": "RETURN",
                  "variable_pos": 0}

return_patterns = [return_pattern_0, return_pattern_1]

literal_pattern = {"PATTERN": Pattern(['NUMBER']),
                      "type": "NUMBER",
                      "variable_pos": 0}

function_stop = {"PATTERN": Pattern(['R_PARENTHESIS']), "type": "INVALID"}
function_pattern = {"PATTERN": Pattern(["VARIABLE", "L_PARENTHESIS"]),
                      "type": "FUNTION",
                      "variable_pos": 0}


simple_patterns = [set_Pattern, line_Pattern, r_bracket, l_bracket]


class StageOneParser:
    #  Takes list of tokens and combines into meta tokens

    def __init__(self, input):
        self.code = input
        self.output = []

        while self.parse_one():
            pass

    def parse_one(self):
        for a in array_patterns:
            if a["PATTERN"].match(self.code):
                name = self.code[a["variable_pos"]][1]
                start = self.code[a["start_index_pos"]]
                stop = self.code[a["stop_index_pos"]]
                self.output.append({"type": a["type"], "name": name, "start": start, "stop": stop})
                self.code = self.code[len(a["PATTERN"]):]
                return True

        if function_pattern["PATTERN"].match(self.code):
            function_name = self.code[function_pattern["variable_pos"]][1]

            self.code = self.code[2:]
            tmp_code = []
            pos = 0
            exit = False
            while not exit:
                if function_stop["PATTERN"].match(self.code[pos:]):
                    exit = True
                else:
                    tmp_code.append(self.code[pos])

                pos += 1
                self.code = self.code[pos:]
            data = []
            for num in tmp_code:
                data.append({"type": num[0], "name": num[1]})
            self.output.append({"type": function_pattern["type"], "name": function_name, "arguments":data})
            return True

        if variable_Pattern_0["PATTERN"].match(self.code):
            variable = self.code[variable_Pattern_0["variable_pos"]][1]
            index = self.code[variable_Pattern_0["index_pos"]][1]
            self.output.append({"type": variable_Pattern_0["type"], "name": variable, "index": index})
            self.code = self.code[4:]
            return True

        if variable_Pattern_1["PATTERN"].match(self.code):
            variable = self.code[variable_Pattern_1["variable_pos"]][1]
            index = self.code[variable_Pattern_1["index_pos"]][1]
            self.output.append({"type": variable_Pattern_1["type"], "name": variable, "index": index})
            self.code = self.code[4:]
            return True

        if variable_Pattern_2["PATTERN"].match(self.code):
            variable = self.code[variable_Pattern_2["variable_pos"]][1]
            self.output.append({"type": variable_Pattern_2["type"], "name": variable})
            self.code = self.code[1:]
            return True

        if literal_pattern["PATTERN"].match(self.code):
            variable = self.code[literal_pattern["variable_pos"]][1]
            self.output.append({"type": literal_pattern["type"], "data": variable})
            self.code = self.code[1:]
            return True

        for r in return_patterns:
            if r["PATTERN"].match(self.code):
                variable = self.code[literal_pattern["variable_pos"]][1]
                self.output.append({"type": literal_pattern["type"], "data": variable})
                self.code = self.code[1:]
                return True

        if array_literal_start_pattern["PATTERN"].match(self.code):
            tmp_code = []
            pos = 1
            count = 1
            while count != 0:
                if array_literal_start_pattern["PATTERN"].match(self.code[pos:]):
                    count += 1
                elif array_literal_stop_pattern["PATTERN"].match(self.code[pos:]):
                    count -= 1
                else:
                    tmp_code.append(self.code[pos])
                pos += 1

            self.code = self.code[pos:]
            data = []
            for num in tmp_code:
                data.append({"type": num[0], "value": num[1]})
            self.output.append({"type": array_literal_start_pattern["type"], "data": data})
            return True

        for p in simple_patterns:
            if p["PATTERN"].match(self.code):
                self.output.append({"type": p["type"]})
                self.code = self.code[1:]
                return True

    def get_list(self):
        return self.output


class TokenParser:
    tree = {"type": "PROGRAM", "body": None}
    current_leaf = tree["body"]

    def __init__(self, input):
        self.code = input

