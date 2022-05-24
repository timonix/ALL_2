code_0 = {"global_variables": {},
          "functions":
              {"main":
                  {"code": [
                      {"return": {"argument": {'type': 'variable', 'name': 'foo'}}}
                  ],
                      "local_variables":
                          {"foo": {
                              "type": "integer",
                              "initial": {'type': 'integer', 'value': 0}}},
                      "arguments": []
                  }
              }
          }

# def main( void ){
#    def foo = int[2] := [0,1]
#    for( j : foo ){
#        j = j+1
#    }
#    return foo
# }

code_1 = {
    "global_variables": {},
    "functions": {
        "main": {
            "code": [
                {
                    "set": {
                        "target": {"type": "index", "name": "j.index"},
                        "expression": {"type": "integer", "value": 0},
                    }
                },
                {"Label": 0},
                {
                    "set": {
                        "target": {"type": "variable", "name": "j"},
                        "expression": {
                            "type": "indexed_variable",
                            "name": "foo",
                            "index": "j.index",
                        },
                    }
                },
                {
                    "set": {
                        "target": {"type": "variable", "name": "j"},
                        "expression": {
                            "type": "add",
                            "left": {"type": "variable", "name": "j"},
                            "right": {"type": "integer", "value": 1},
                        },
                    }
                },
                {
                    "if": {
                        "target_label": 0,
                        "expression": {
                            "type": "not_equals",
                            "left": {"type": "index", "name": "j.index"},
                            "right": {"type": "integer", "value": 1},
                        },
                    }
                },
                {"return": {"argument": {"type": "variable", "name": "foo"}}},
            ],
            "local_variables": {
                "j": {"type": "integer"},
                "j.index": {"type": "index"},
                "foo": {
                    "type": "integer_array",
                    "length": 2,
                    "initial": {"type": "integer_array", "value": [0, 1]},
                },
            },
            "arguments": [],
        }
    },
}

