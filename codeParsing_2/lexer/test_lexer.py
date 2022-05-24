import sys
import unittest
from os.path import join

import lexer
sys.path.append("..")

from TestCode import post_lexer


class TestTokenParser(unittest.TestCase):

    def test_func(self):
        for test in post_lexer.tests.items():
            key = test[1]
            f = open(join("../TestCode", test[0]), "r")
            test = lexer.make_string_code_into_list(f.read())
            f.close()
            self.assertEqual(key, test)

