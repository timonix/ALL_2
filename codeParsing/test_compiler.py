import math
import unittest
import compiler


class TestCompiler(unittest.TestCase):

    def test_simple(self):
        constants = {'a': {'type': 'i', 'value': '127'}, 'b': {'type': 'F', 'value': ['1.5', '2.0']}, 'c': {'type': 'A', 'value': '4'}}
        constants, memory = compiler.machine_code_from_constants(constants)

        self.assertEqual({'a': {'type': 'i', 'value': '127', 'location': 1}, 'b': {'type': 'F', 'value': ['1.5', '2.0'], 'location': 2}, 'c': {'type': 'A', 'value': '4', 'location': 4}},constants)
        self.assertEqual([127, 6144, 8192, 0, 0, 0, 0], memory)

    def test_float_toBinary(self):
        test = compiler.floatToBinary(1.5)
        self.assertEqual(6144, test)

    def test_float_to_binary_lossy(self):
        test = compiler.floatToBinary(math.pi)
        self.assertEqual(12868, test)

    def test_double_to_binary_lossy(self):
        test0 = compiler.doubleToBinaryHigh(math.pi)
        test1 = compiler.doubleToBinaryLow(math.pi)
        self.assertEqual(3, test0)
        self.assertEqual(2375531, test1)

    def test_main_function(self):
        consts = {'a': {'type': 'i', 'value': '0'}}
        constants, memory = compiler.machine_code_from_constants(consts)
        code = {'main': {'args': 0, 'code': ['q=1', 'a=1', "returnq"]}}
        compiler.assembly_from_function(code, constants, memory)
