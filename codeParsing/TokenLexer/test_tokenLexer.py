import unittest

from TokenLexer import TokenLexer
import testCodePostLexer


class TestFindBraces(unittest.TestCase):

    def test_simple(self):
        code = "A=0\n" \
               "B=1"
        lex = TokenLexer(code)

        self.assertEqual(('VARIABLE', 'A'), lex.next_token())
        self.assertEqual('VAL_SET', lex.next_token())
        self.assertEqual(('NUMBER', 0), lex.next_token())
        self.assertEqual("LINE", lex.next_token())
        self.assertEqual(('VARIABLE', 'B'), lex.next_token())
        self.assertEqual('VAL_SET', lex.next_token())
        self.assertEqual(('NUMBER', 1), lex.next_token())

    def test_list(self):
        code = "if(AA_SD10==1){\n" \
               "B66A_SD=1.5\n" \
               "}"
        lex = TokenLexer(code)
        test = lex.get_list()
        target = ['IF', 'L_PARENTHESIS',
                  ('VARIABLE', 'AA_SD10'), 'EQUALITY_TEST', ('NUMBER', 1),
                  'R_PARENTHESIS', 'L_BRACKET', 'LINE',
                  ('VARIABLE', 'B66A_SD'), 'VAL_SET', ('NUMBER', 1.5),
                  'LINE', 'R_BRACKET']
        self.assertEqual(target, test)

    def test_vector(self):
        code = "ASD = <1.5d, <3.7, 7>>"
        lex = TokenLexer(code)
        test = lex.get_list()
        target = [('VARIABLE', 'ASD'), 'VAL_SET',
                  'L_ARROW', ('DOUBLE', 1.5),
                  'COMMA', 'L_ARROW', ('NUMBER', 3.7), 'COMMA', ('NUMBER', 7),
                  'R_ARROW', 'R_ARROW']
        self.assertEqual(target, test)

    def test_indexing_into_vector(self):
        code = "ASD = <1.5d, <3.7, 7>>\n" \
               "a = ASD[0..1]\n" \
               ""
        lex = TokenLexer(code)
        test = lex.get_list()
        target = [('VARIABLE', 'ASD'), 'VAL_SET',
                  'L_ARROW', ('DOUBLE', 1.5), 'COMMA',
                  'L_ARROW', ('NUMBER', 3.7), 'COMMA',
                  ('NUMBER', 7), 'R_ARROW', 'R_ARROW',
                  'LINE', ('VARIABLE', 'a'), 'VAL_SET',
                  ('VARIABLE', 'ASD'), 'L_INDEXING',
                  ('NUMBER', 0), 'TO', ('NUMBER', 1),
                  'R_INDEXING', 'LINE']

        self.assertEqual(target, test)

    def test_lex_from_file(self):

        lex = TokenLexer.open("../testCode2")
        self.assertEqual(testCodePostLexer.testCode2, lex.get_list())
        lex = TokenLexer.open("../testCode3")
        self.assertEqual(testCodePostLexer.testCode3, lex.get_list())
