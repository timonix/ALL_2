import unittest
import jvm
from OPCODES import *
import OPCODES

class TestOpcodes(unittest.TestCase):
    def test_add_const_to_stack(self):
        stack = [None]*10
        jvm.executeMethod([ICONST_1], [], stack, 0)
        self.assertEqual(stack[0], 1)

    def test_add_two(self):
        stack = [None]*10
        code = [ICONST_1, ICONST_1, IADD, IRETURN]
        jvm.executeMethod(code, [], stack, 0)
        self.assertEqual(stack[0], 2)

    def test_byte_add(self):
        stack = [None] * 10
        stack[0] = 12345
        code = [BIPUSH, 0x10, ISTORE_1, BIPUSH, 0x20, ISTORE_2, ILOAD_1, ILOAD_2, IADD, IRETURN]
        jvm.executeMethod(code, [], stack, 1)
        self.assertEqual(stack[1], 0x30)
        self.assertEqual(stack[0], 12345)


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
