import unittest

import lexer
from extractor import Extractor

class TestFindBraces(unittest.TestCase):

    def test_simple(self):
        ex = Extractor()
        code = ['a=0', 'main(0)', ['q=1', 'fun(q)'], 'b=<1.0,2.0>F', "c=<4>A", 'fun(1)', ['returna']]
        ex.extract_globals(code)

        self.assertEqual({'main': {'args': 0, 'code': ['q=1', 'fun(q)']}, 'fun': {'args': 1, 'code': ['returna']}}, ex.function_dict)
        self.assertEqual({'a': {'type': 'i', 'value': '0'}, 'b': {'type': 'F', 'value': ['1.0', '2.0']}, 'c': {'type': 'A', 'value': '4'}}, ex.global_dict)

    def test_func(self):

        f = open("testCode2", "r")
        test = lexer.make_string_code_into_list(f.read())
        f.close()
        self.assertEqual(['a=0', 'main()', ['q=1', 'fun(q)'], 'fun(a)', ['returna']], test)



if __name__ == '__main__':
    unittest.main()