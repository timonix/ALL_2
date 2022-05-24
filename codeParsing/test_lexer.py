import unittest

import lexer

class TestFindBraces(unittest.TestCase):

    def test_single_line(self):
        code = "q = 0"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(["q=0"], test)

    def test_double_line(self):
        code = "q = 0\n" \
               "w = 1"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(["q=0", "w=1"], test)

    def test_if(self):
        code = "if(a == 0){\n" \
               "w = 1\n" \
               "}"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(["if(a==0)", ["w=1"]], test)

    def test_nested_if(self):
        code = "if(a == 0){\n" \
               "\tw = 1\n" \
               "\tif(b == 0){\n" \
               "\t\tb = 2\n" \
               "}" \
               "}"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(['if(a==0)', ['w=1', 'if(b==0)', ['b=2']]], test)

    def test_for(self):
        code = "for(a : 0 to 10){\n" \
               "w = w+1\n" \
               "}"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(['for(a:0>to>10)', ['w=w+1']], test)

    def test_empty_frame(self):
        code = "(){\n}"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(['()', []], test)

    def test_empty_lines(self):
        code = "a= 1\n" \
               "\n" \
               "b=2"
        test = lexer.make_string_code_into_list(code)
        self.assertEqual(["a=1", "b=2"], test)

    def test_code_from_file(self):
        f = open("testCode1", "r")
        test = lexer.make_string_code_into_list(f.read())
        f.close()
        self.assertEqual(["q=0", "for(element:list,q)", ["asd1", "line21"]], test)

    def test_func(self):
        f = open("testCode2", "r")
        test = lexer.make_string_code_into_list(f.read(), log_level=True)
        f.close()
        print(test)
        self.assertEqual(['a=0', 'main()', ['q=1', 'fun(q)'], 'fun(a)', ['returna']], test)


if __name__ == '__main__':
    unittest.main()