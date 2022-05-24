class cpu:
    C_memory_delay = 1

    stage = 0

    R_Data_memory_write = 0
    R_Return_memory_write = 0
    R_Stack_pointer = 1
    R_Frame_pointer = 0
    R_Program_counter = 0
    R_Return_Pointer = 0
    R_Memory_address = 0

    R_A0 = 0
    R_A1 = 0
    R_B0 = 0
    R_B1 = 0

    R_R1 = 0
    R_R2 = 0

    M_data = [None] * 100
    M_return_stack = [None] * 100

    stage2_add = False
    stage2_mul = False
    stage2_LD_LA = False
    stage2_LD_LB = False
    stage2_LD_OA = False
    stage2_LD_OB = False

    alu_tmp = None

    ValidConditions = [None] * 16

    def run_code(self, code, debug=False):
        stop = False
        if debug:
            print("starting at:" + str(self.R_Program_counter))
        while self.R_Program_counter < len(code) and not stop:
            if debug:
                print(str(self.R_Program_counter) + " : " + str(code[self.R_Program_counter]))
            stop = self.run_instruction(code[self.R_Program_counter][0], code[self.R_Program_counter][1])
        if debug:
            print("STOP:" + str(stop))

    def run_instruction(self, ins, arg):
        if self.stage2_add:
            self.R_R1 = self.alu_tmp & 0xFFFFFF
            self.R_R2 = (self.alu_tmp & (0xFFFFFF << 24)) >> 24
            self.stage2_add = False
        if self.stage2_LD_LA:
            self.R_A0 = self.M_data[self.R_Memory_address]
            self.stage2_LD_LA = False
        if self.stage2_LD_LB:
            self.R_B0 = self.M_data[self.R_Memory_address]
            self.stage2_LD_LB = False
        if self.stage2_LD_OA:
            self.R_A0 = self.M_data[self.R_Memory_address]
            self.stage2_LD_OA = False
        if self.stage2_LD_OB:
            self.R_B0 = self.M_data[self.R_Memory_address]
            self.stage2_LD_OB = False

        if ins == "LDI_A": # TODO sign extend
            self.R_A0 = arg
            self.R_Program_counter += 1
        elif ins == "LDI_B":
            self.R_B0 = arg
            self.R_Program_counter += 1
        elif ins == "LDI_0_B":
            self.R_B0 = 0
            self.R_Program_counter += 1
        elif ins == "LDI_0_A":
            self.R_A0 = 0
            self.R_Program_counter += 1
        elif ins == "LDI_1_B":
            self.R_B0 = 1
            self.R_Program_counter += 1
        elif ins == "LDI_1_A":
            self.R_A0 = 1
            self.R_Program_counter += 1
        elif ins == "LDI_M1_B":
            self.R_B0 = -1
            self.R_Program_counter += 1
        elif ins == "LDI_M1_A":
            self.R_A0 = -1
            self.R_Program_counter += 1
        elif ins == "ADD":
            self.alu_tmp = (self.R_A0 | (self.R_A1 << 24)) + (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "MUL":
            self.alu_tmp = self.R_A0 * self.R_B0
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "MUL_L":
            self.alu_tmp = (self.R_A0 | (self.R_A1 << 24)) * (self.R_B0 | (self.R_B1 << 24)) >> 24
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "OR":
            self.alu_tmp = (self.R_A0 | (self.R_A1 << 24)) | (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "NOR":
            self.alu_tmp = ~(self.R_A0 | (self.R_A1 << 24)) | (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "AND":
            self.alu_tmp = (self.R_A0 | (self.R_A1 << 24)) & (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "NAND":
            self.alu_tmp = ~(self.R_A0 | (self.R_A1 << 24)) & (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "XOR":
            self.alu_tmp = (self.R_A0 | (self.R_A1 << 24)) ^ (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "XNOR":
            self.alu_tmp = ~(self.R_A0 | (self.R_A1 << 24)) ^ (self.R_B0 | (self.R_B1 << 24))
            self.stage2_add = True
            self.R_Program_counter += 1
        elif ins == "D_ALLOC":
            self.R_Stack_pointer += arg
            self.R_Program_counter += 1
        elif ins == "D_ALLOC_DYN":
            self.R_Stack_pointer += self.R_A0
            self.R_Program_counter += 1
        elif ins == "ST_LA0":
            self.M_data[self.R_Frame_pointer + arg] = self.R_A0
            self.R_Program_counter += 1
        elif ins == "ST_LB0":
            self.M_data[self.R_Frame_pointer + arg] = self.R_B0
            self.R_Program_counter += 1
        elif ins == "ST_LA1":
            self.M_data[self.R_Frame_pointer + arg] = self.R_A1
            self.R_Program_counter += 1
        elif ins == "ST_LB1":
            self.M_data[self.R_Frame_pointer + arg] = self.R_B1
            self.R_Program_counter += 1
        elif ins == "ST_LR1":
            self.M_data[self.R_Frame_pointer + arg] = self.R_R1
            self.R_Program_counter += 1
        elif ins == "ST_LR2":
            self.M_data[self.R_Frame_pointer + arg] = self.R_R2
            self.R_Program_counter += 1
        elif ins == "ST_LRM":
            self.M_data[self.R_Frame_pointer + arg] = (self.R_R1 & 0xFFF000) >> 12 | (self.R_R2 & 0x000FFF) << 12
            self.R_Program_counter += 1
        elif ins == "ST_FP":
            self.M_data[self.R_Frame_pointer + arg] = self.R_Frame_pointer
            self.R_Program_counter += 1
        elif ins == "NOP":
            self.R_Program_counter += 1
            pass
        elif ins == "LD_OA":
            self.R_Memory_address = arg + self.R_A0
            self.stage2_LD_OA = True
            self.R_Program_counter += 1
        elif ins == "LD_OB":
            self.R_Memory_address = arg + self.R_A0
            self.stage2_LD_OB = True
            self.R_Program_counter += 1
        elif ins == "LD_LA":
            self.R_Memory_address = arg + self.R_Frame_pointer
            self.stage2_LD_LA = True
            self.R_Program_counter += 1
        elif ins == "LD_LB":
            self.R_Memory_address = arg + self.R_Frame_pointer
            self.stage2_LD_LB = True
            self.R_Program_counter += 1
        elif ins == "CALL":
            self.R_Return_memory_write = self.R_Program_counter + 1
            self.M_return_stack[self.R_Return_Pointer] = self.R_Return_memory_write
            self.R_Data_memory_write = self.R_Frame_pointer
            self.R_Memory_address = self.R_Stack_pointer
            self.M_data[self.R_Memory_address] = self.R_Data_memory_write
            self.R_Frame_pointer = self.R_Stack_pointer
            self.R_Program_counter = arg
            self.R_Return_Pointer += 1
        elif ins == "BREAK":
            self.R_Program_counter += 1
            return True
        elif ins == "RETURN":
            self.R_Program_counter = self.M_return_stack[self.R_Return_Pointer - 1]
            self.R_Return_Pointer -= 1

            self.R_Stack_pointer = self.R_Frame_pointer
            self.R_Memory_address = self.R_Frame_pointer

            # STAGE 2
            self.R_Frame_pointer = self.M_data[self.R_Memory_address]
        elif ins == "MOV_R1_A0":
            self.R_A0 = self.R_R1
            self.R_Program_counter += 1
        elif ins == "MOV_R2_A0":
            self.R_A0 = self.R_R2
            self.R_Program_counter += 1
        elif ins == "MOV_R1_B0":
            self.R_B0 = self.R_R1
            self.R_Program_counter += 1
        elif ins == "MOV_R2_B0":
            self.R_B0 = self.R_R2
            self.R_Program_counter += 1
        elif ins == "MOV_R1_A1":
            self.R_A1 = self.R_R1
            self.R_Program_counter += 1
        elif ins == "MOV_R2_A1":
            self.R_A1 = self.R_R2
            self.R_Program_counter += 1
        elif ins == "MOV_R1_B1":
            self.R_B1 = self.R_R1
            self.R_Program_counter += 1
        elif ins == "MOV_R2_B1":
            self.R_B1 = self.R_R2
            self.R_Program_counter += 1
        elif ins == "MOV_RM_B0":
            self.R_B0 = (self.R_R1 & 0xFFF000) >> 12 | (self.R_R2 & 0x000FFF) << 12
            self.R_Program_counter += 1
        elif ins == "MOV_RM_A0":
            self.R_A0 = (self.R_R1 & 0xFFF000) >> 12 | (self.R_R2 & 0x000FFF) << 12
            self.R_Program_counter += 1
        elif ins == "MOV_R_A":
            self.R_A0 = self.R_R1
            self.R_A1 = self.R_R2
            self.R_Program_counter += 1
        elif ins == "MOV_R_B":
            self.R_B0 = self.R_R1
            self.R_B1 = self.R_R2
            self.R_Program_counter += 1

        elif ins == "MOV_A0_A1":
            self.R_A1 = self.R_A0
            self.R_Program_counter += 1
        elif ins == "MOV_A1_A0":
            self.R_A0 = self.R_A1
            self.R_Program_counter += 1
        elif ins == "MOV_B1_B0":
            self.R_B0 = self.R_B1
            self.R_Program_counter += 1
        elif ins == "MOV_B0_B1":
            self.R_B1 = self.R_B0
            self.R_Program_counter += 1
        elif ins == "MOV_A_B":
            self.R_B0 = self.R_A0
            self.R_B1 = self.R_A1
            self.R_Program_counter += 1
        elif ins == "MOV_B_A":
            self.R_A0 = self.R_B0
            self.R_A1 = self.R_B1
            self.R_Program_counter += 1
        elif ins == "BRA":  # TODO Test
            offset = arg & 0x0FFFFF
            condition = (arg & 0xF00000) >> 20
            if self.ValidConditions[condition]:
                self.R_Program_counter += offset
        elif ins == "EXT_A":  # TODO Test
            if self.R_A0 & 0x800000 != 0:
                self.R_A1 = 0xFFFFFF
            else:
                self.R_A1 = 0x000000
        elif ins == "EXT_B":  # TODO Test
            if self.R_B0 & 0x800000 != 0:
                self.R_B1 = 0xFFFFFF
            else:
                self.R_B1 = 0x000000

            # always
            # zero
            # zero'
            # carry
            # carry'
            # negative
            # negative'
            # greater than
            # less than
            # greater or equal
            # less or equal
            # equal
            # not equal

        else:
            print("Bad instruction:" + ins)
            assert (False)
