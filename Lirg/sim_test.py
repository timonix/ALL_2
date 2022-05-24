import unittest
import random

from sim import cpu


class TestOpcodes(unittest.TestCase):

    def test_load_const_to_A0(self):
        my_cpu = cpu()
        my_cpu.run_instruction("LDI_A", 10)
        self.assertEqual(my_cpu.R_A0, 10)

    def test_ADD_two_small_constants(self):
        my_cpu = cpu()
        for i in range(100):
            c1 = random.randint(0, 0xFFFFFF)
            c2 = random.randint(0, 0xFFFFFF)
            my_cpu.run_instruction("LDI_A", c1)
            my_cpu.run_instruction("LDI_B", c2)
            self.assertEqual(my_cpu.R_A0, c1)
            self.assertEqual(my_cpu.R_B0, c2)
            my_cpu.run_instruction("ADD", c2)
            my_cpu.run_instruction("NOP", c2)

            self.assertEqual((c1 + c2) & 0xFFFFFF, my_cpu.R_R1)
            self.assertEqual((c1 + c2) >> 24, my_cpu.R_R2)
            self.assertEqual(0, my_cpu.R_R2 & 0xFFFFFE)

    def test_create_local_variable(self):
        my_cpu = cpu()
        my_cpu.run_instruction("D_ALLOC", 1)
        my_cpu.run_instruction("LDI_A", 44)
        my_cpu.run_instruction("ST_LA0", 1)
        self.assertEqual(0, my_cpu.R_Frame_pointer)
        self.assertEqual(44, my_cpu.M_data[1])
        self.assertEqual(2, my_cpu.R_Stack_pointer)

    def test_code_run(self):
        my_cpu = cpu()
        code = [["D_ALLOC", 1],
                ["LDI_A", 44],
                ["ST_LA0", 1]]
        my_cpu.run_code(code)
        self.assertEqual(0, my_cpu.R_Frame_pointer)
        self.assertEqual(44, my_cpu.M_data[1])
        self.assertEqual(2, my_cpu.R_Stack_pointer)

    def test_OR_two_local_variables(self):
        for i in range(100):
            c1 = random.randint(0, 0xFFFFFF)
            c2 = random.randint(0, 0xFFFFFF)

            my_cpu = cpu()
            my_cpu.run_instruction("D_ALLOC", 2)
            my_cpu.run_instruction("LDI_A", c1)
            my_cpu.run_instruction("ST_LA0", 1)
            my_cpu.run_instruction("LDI_A", c2)
            my_cpu.run_instruction("ST_LA0", 2)
            self.assertEqual(c1, my_cpu.M_data[1])
            self.assertEqual(c2, my_cpu.M_data[2])
            self.assertEqual(3, my_cpu.R_Stack_pointer)

            my_cpu.run_instruction("LD_LA", 1)
            my_cpu.run_instruction("LD_LB", 2)
            my_cpu.run_instruction("OR", None)
            my_cpu.run_instruction("NOP", None)

            self.assertEqual(c1 | c2, my_cpu.R_R1)

    def test_call_global_function(self):
        my_cpu = cpu()
        my_cpu.run_instruction("D_ALLOC", 0x05)
        my_cpu.run_instruction("CALL", 0x55)
        self.assertEqual(2, my_cpu.M_return_stack[0])
        self.assertEqual(1, my_cpu.R_Return_Pointer)
        self.assertEqual(6, my_cpu.R_Frame_pointer)
        my_cpu.run_instruction("LDI_A", 77)
        my_cpu.run_instruction("ST_LA0", 1)
        self.assertEqual(77, my_cpu.M_data[my_cpu.R_Frame_pointer + 1])
        my_cpu.run_instruction("RETURN", None)
        self.assertEqual(0, my_cpu.R_Frame_pointer)

    def test_run_call_with_local_reference(self):
        my_cpu = cpu()
        code = [["D_ALLOC", 0x03],
                ["LDI_A", 0x10],
                ["ST_LA0", 1],
                ["ST_FP", 3],
                ["CALL", 8],
                ["NOP", None],
                ["NOP", None],
                ["NOP", None],
                ["BREAK", None],  # call target
                ["LD_LA", -1],
                ["NOP", None],
                ["LD_OB", 1],
                ["D_ALLOC", 4],
                ["ST_LB0", 4],
                ["NOP", None],
                ["NOP", None]
                ]

        my_cpu.run_code(code)
        self.assertEqual(9, my_cpu.R_Program_counter)
        my_cpu.run_code(code)
        self.assertEqual(0x10, my_cpu.M_data[8])

    def test_moves(self):
        my_cpu = cpu()
        for i in range(100):
            c1 = random.randint(0, 0xFFFFFF)
            c2 = random.randint(0, 0xFFFFFF)
            code = [["LDI_A", c1],
                    ["BREAK", None],
                    ["MOV_A0_A1", None],
                    ["MOV_A_B", None],
                    ["BREAK", None],  # check asserts
                    ["LDI_B", c2],
                    ["MOV_B0_B1", None],
                    ["XOR", None],
                    ["BREAK", None],
                    ["MOV_R1_B0", None],
                    ["MOV_R2_B1", None],
                    ["MOV_R1_A0", None],
                    ["MOV_R2_A1", None]
                    ]
            my_cpu.R_Program_counter = 0
            my_cpu.run_code(code)
            self.assertEqual(c1, my_cpu.R_A0)
            my_cpu.run_code(code)
            self.assertEqual(c1, my_cpu.R_A1)

            self.assertEqual(my_cpu.R_A0, my_cpu.R_A1)
            self.assertEqual(my_cpu.R_B0, my_cpu.R_B1)
            self.assertEqual(my_cpu.R_A1, my_cpu.R_B1)
            my_cpu.run_code(code)
            self.assertEqual(my_cpu.R_B0, my_cpu.R_B1)
            my_cpu.run_code(code)
            self.assertEqual(my_cpu.R_B0, my_cpu.R_A0)
            self.assertEqual(my_cpu.R_B1, my_cpu.R_A1)
            self.assertEqual(my_cpu.R_R1, my_cpu.R_A0)
            self.assertEqual(my_cpu.R_R2, my_cpu.R_A1)
            self.assertEqual(c1 ^ c2, my_cpu.R_A0)
            self.assertEqual(c1 ^ c2, my_cpu.R_A1)

    def test_mul_small(self):
        my_cpu = cpu()
        for i in range(100):
            c1 = random.randint(0, 0xFFFFFF)
            c2 = random.randint(0, 0xFFFFFF)
            code = [["LDI_A", c1],
                    ["LDI_B", c2],
                    ["MUL", None],
                    ["NOP", None]
                    ]
            my_cpu.R_Program_counter = 0
            my_cpu.run_code(code)
            self.assertEqual(c1 * c2, (my_cpu.R_R2 << 24) | my_cpu.R_R1)

    def test_mul_large(self):
        my_cpu = cpu()
        for i in range(100):
            c1 = random.randint(0, 0xFFFFFF)
            c2 = random.randint(0, 0xFFFFFF)
            c3 = random.randint(0, 0xFFFFFF)
            c4 = random.randint(0, 0xFFFFFF)

            code = [["LDI_A", c1],
                    ["LDI_B", c2],
                    ["MOV_A0_A1", None],
                    ["MOV_B0_B1", None],
                    ["LDI_A", c3],
                    ["LDI_B", c4],
                    ["MUL_L", None],
                    ["NOP", None]
                    ]
            my_cpu.R_Program_counter = 0
            my_cpu.run_code(code)

            left = (c1 << 24) | c3
            right = (c2 << 24) | c4
            self.assertEqual((left*right) >> 24 & 0xFFFFFFFFFFFF, (my_cpu.R_R2 << 24) | my_cpu.R_R1)
