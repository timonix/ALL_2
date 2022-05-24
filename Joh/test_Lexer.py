import unittest
import random

import Lexer
import post_lexer


class TestOpcodes(unittest.TestCase):
    def test_code_0(self):
        f = open("code_0.joh", "r")
        res = Lexer.lex(f.read())
        f.close()
        self.assertEqual(post_lexer.code_0, res)

    def test_code_1(self):
        f = open("code_1.joh", "r")
        res = Lexer.lex(f.read())
        f.close()
        self.assertEqual(post_lexer.code_1, res)

    def test_code_2(self):
        f = open("code_2.joh", "r")
        res = Lexer.lex(f.read())
        f.close()
        self.assertEqual(post_lexer.code_2, res)
