import unittest
import random

import Parser
import post_lexer
import post_parser


class TestOpcodes(unittest.TestCase):
    def test_code_0(self):
        res = Parser.parse(post_lexer.code_0)
        self.assertEqual(post_parser.code_0, res)

    def test_code_1(self):
        res = Parser.parse(post_lexer.code_1)
        self.assertEqual(post_parser.code_1, res)
