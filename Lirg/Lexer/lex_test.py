import unittest
import random

import lex


class TestOpcodes(unittest.TestCase):
    def test_from_file(self):
        ll = lex.file_to_list("testCode")
        target = ['a=1', 'constb=10', 'if(a!=0)', ['for(i:0>to>b;a)', ['a=a+1', '(a)', ['qq=1']]]]
        self.assertEqual(target, ll)
