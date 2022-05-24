import re

# takes a file or string extracts a list of tokens

# regex to identify:Type of data
keywords = {r"^if": "IF",
            r"^for": "FOR_LOOP",
            r"^return": "RETURN",
            r"^while": "WHILE"}

separators = {r"^}": "R_BRACKET",
              r"^{": "L_BRACKET",
              r"^\)": "R_PARENTHESIS",
              r"^\(": "L_PARENTHESIS",
              r"^\[": "L_INDEXING",
              r"^\]": "R_INDEXING",
              r"^<": "L_ARROW",
              r"^>": "R_ARROW",
              r"^\,": "COMMA",
              r"^\n": "LINE"}

operators = {r"^\+": "ADD",
             r"^\-": "SUB",
             r"^\*": "MUL",
             r"^\==": "EQUALITY_TEST",
             r"^\=": "VAL_SET",
             r"^\.\.": "TO"}

literal = {r"^true": "TRUE",
           r"^false": "FALSE",
           r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+\-]?\d+)?d": "DOUBLE",
           r"^\d*l": "LONG",
           r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+\-]?\d+)?": "NUMBER"}

identifier = {r"^\w*": "VARIABLE"}


class TokenLexer:

    def __init__(self, code):
        assert isinstance(code, str), 'Argument of wrong type!'
        self.code = code.replace(" ", "")
        self.last_token = None

    def get_list(self):
        list = []
        next_t = self.next_token()
        while next_t:
            list.append(next_t)
            next_t = self.next_token()
        return list

    @staticmethod
    def open(file_path):
        f = open(file_path, "r")
        lex = TokenLexer(f.read())
        f.close()
        return lex

    def next_token(self):
        if len(self.code) == 0:
            return None

        for regex, token_type in keywords.items():
            match = re.search(regex, self.code)
            if match:
                self.last_token = token_type
                self.code = self.code[match.end():]
                return self.last_token

        for regex, token_type in separators.items():
            match = re.search(regex, self.code)
            if match:
                self.last_token = token_type
                self.code = self.code[match.end():]
                return self.last_token

        for regex, token_type in operators.items():
            match = re.search(regex, self.code)
            if match:
                self.last_token = token_type
                self.code = self.code[match.end():]
                return self.last_token

        for regex, token_type in literal.items():

            match = re.search(regex, self.code)
            if match and match.end() != 0:
                val = self.code[match.start(): match.end()]
                if token_type == "NUMBER" and "." in val:
                    self.last_token = (token_type, float(val))
                elif token_type == "NUMBER":
                    self.last_token = (token_type, int(val))
                elif token_type == "LONG":
                    self.last_token = (token_type, int(val[:-1]))
                elif token_type == "DOUBLE":
                    self.last_token = (token_type, float(val[:-1]))
                else:
                    self.last_token = (token_type, self.code[match.start(): match.end()])
                self.code = self.code[match.end():]
                return self.last_token

        for regex, token_type in identifier.items():
            match = re.search(regex, self.code)
            if match and match.end() != 0:
                self.last_token = (token_type, self.code[match.start(): match.end()])
                self.code = self.code[match.end():]
                return self.last_token

        assert False, "no match to token:" + self.code

# output {Type, value}
