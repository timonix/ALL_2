import unittest
from TokenParser import TokenParser, Pattern, StageOneParser


import sys
sys.path.append("..")

from TokenLexer import testCodePostLexer



class TestTokenParser(unittest.TestCase):

    def test_pattern_matching(self):
        pat = Pattern(['VARIABLE', 'VAL_SET', 'NUMBER'])
        self.assertTrue(pat.match([('VARIABLE', 'b'), 'VAL_SET', ('NUMBER', 4)]))
        self.assertTrue(pat.match([('VARIABLE', 'a'), 'VAL_SET', ('NUMBER', 1)]))

    def test_stage_1(self):
        # A = B[0]
        code = [("VARIABLE", "A"), "VAL_SET", ("VARIABLE", "B"), "L_INDEXING", ("NUMBER", 0), "R_INDEXING"]
        stage_1 = StageOneParser(code)
        self.assertEqual([{'type': 'VARIABLE', 'name': 'A'}, {'type': 'VAL_SET'},
                          {'type': 'VARIABLE_INDEXED', 'name': 'B', 'index': 0}], stage_1.get_list())
        self.assertEqual([], stage_1.code)

    def test_stage_1_array(self):
        # A = B[0]
        code = [("VARIABLE", "B"), "L_INDEXING", ("NUMBER", 0), "TO", ("NUMBER", 1), "R_INDEXING", "VAL_SET",
                ("VARIABLE", "B"), "L_INDEXING", ("NUMBER", 1), "TO", ("NUMBER", 0), "R_INDEXING"]
        stage_1 = StageOneParser(code)

        self.assertEqual(
            [{'type': 'ARRAY', 'name': 'B', 'start': ('NUMBER', 0), 'stop': ('NUMBER', 1)}, {'type': 'VAL_SET'},
             {'type': 'ARRAY', 'name': 'B', 'start': ('NUMBER', 1), 'stop': ('NUMBER', 0)}]
            , stage_1.get_list())
        self.assertEqual([], stage_1.code)

    def test_stage_1_literal_array(self):
        code = [("VARIABLE", "B"), "L_INDEXING", ("NUMBER", 0), "TO", ("NUMBER", 1), "R_INDEXING", "VAL_SET",
                "L_ARROW", ("NUMBER", 1), ("NUMBER", 0), "R_ARROW"]
        stage_1 = StageOneParser(code)

        self.assertEqual(
            [{'type': 'ARRAY', 'name': 'B', 'start': ('NUMBER', 0), 'stop': ('NUMBER', 1)}, {'type': 'VAL_SET'},
             {'type': 'ARRAY_LITERAL', 'data': [{'type': 'NUMBER', 'value': 1}, {'type': 'NUMBER', 'value': 0}]}]
            , stage_1.get_list())
        self.assertEqual([], stage_1.code)

    def test_stage_1_testcode2(self):
        code = testCodePostLexer.testCode2
        stage_1 = StageOneParser(code)
        print(code)
        print(stage_1.get_list())
        print(stage_1.code)
