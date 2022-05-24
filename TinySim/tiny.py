import copy

registers = {
    "REG_A": 0, "REG_B": 0, "REG_T": 0,
    "PORT": 0, "RAM_IN": 0, "RAM_OUT": 0, "ROM_OUT": 0,
    "MEMORY_ADDRESS": 0, "PROGRAM_COUNTER": 0,
    "MA_H": 0, "MA_L": 0, "PC_H": 0, "PC_L": 0,
    "TIMER": 0
}

registers_next = {
    "REG_A": 0, "REG_B": 0, "REG_T": 0,
    "PORT": 0, "RAM_IN": 0, "RAM_OUT": 0, "ROM_OUT": 0,
    "MEMORY_ADDRESS": 0, "PROGRAM_COUNTER": 0,
    "MA_H": 0, "MA_L": 0, "PC_H": 0, "PC_L": 0,
    "TIMER": 0
}

control = {
    "REG_A": 0, "REG_B": 0, "REG_T": 0,
    "PORT": 0, "RAM_IN": 0, "RAM_OUT": 0, "ROM_OUT": 0,
    "MEMORY_ADDRESS": 0, "PROGRAM_COUNTER": 0,
    "MA_H": 0, "MA_L": 0, "PC_H": 0, "PC_L": 0,
    "TIMER": 0
}

CONTROL_ZEROS = copy.deepcopy(control)

control_next = {
    "REG_A": 0, "REG_B": 0, "REG_T": 0,
    "PORT": 0, "RAM_IN": 0, "RAM_OUT": 0, "ROM_OUT": 0,
    "MEMORY_ADDRESS": 0, "PROGRAM_COUNTER": 0,
    "MA_H": 0, "MA_L": 0, "PC_H": 0, "PC_L": 0,
    "TIMER": 0
}


def update():
    global registers
    global control
    registers = copy.deepcopy(registers_next)
    control = copy.deepcopy(control_next)


def normal_reg_update(register):
    if control[register] == 0:
        pass  # no change
    elif control[register] == 1:
        registers_next[register] = registers["PORT"]
    elif control[register] == 2:
        registers_next[register] = registers["REG_B"]
    elif control[register] == 3:
        registers_next[register] = registers["REG_A"]
    elif control[register] == 4:
        registers_next[register] = registers["RAM_OUT"]
    elif control[register] == 5:
        registers_next[register] = registers["ROM_OUT"]
    elif control[register] == 6:
        registers_next[register] = registers["REG_T"]
    elif control[register] == 7:
        registers_next[register] = registers[register] + 1
    registers_next[register] = registers_next[register] & 255


def pc_update():
    if control["PROGRAM_COUNTER"] == 0:
        registers_next["PROGRAM_COUNTER"] = registers["PROGRAM_COUNTER"] + 1
    elif control["PROGRAM_COUNTER"] == 1:  # jmp
        registers_next["PROGRAM_COUNTER"] = registers["PC_H"] * 256 + registers["PC_L"]
    elif control["PROGRAM_COUNTER"] == 2:  # jmpi
        registers_next["PROGRAM_COUNTER"] = registers["PC_H"] * 256 + registers["ROM_OUT"]
    elif control["PROGRAM_COUNTER"] == 3:  # halt
        registers_next["PROGRAM_COUNTER"] = registers["PROGRAM_COUNTER"]


def pc_reg_update(register):
    if control[register] == 0:
        pass  # no change
    elif control[register] == 1:
        pass  # no change
    elif control[register] == 2:
        registers_next[register] = registers["REG_B"]
    elif control[register] == 3:
        registers_next[register] = registers["REG_A"]
    elif control[register] == 4:
        registers_next[register] = registers["RAM_OUT"]
    elif control[register] == 5:
        registers_next[register] = registers["ROM_OUT"]
    elif control[register] == 6:
        registers_next[register] = registers["REG_T"]
    elif control[register] == 7:
        if registers["PC_L"] == 255:
            registers_next["PC_H"] = registers["PC_H"] + 1
            registers_next["PC_L"] = 0
        else:
            registers_next["PC_L"] = registers_next["PC_L"] + 1

    registers_next[register] = registers_next[register] & 255



def ma_reg_update(register):
    if control[register] == 0:
        pass  # no change
    elif control[register] == 1:
        pass  # no change
    elif control[register] == 2:
        registers_next[register] = registers["REG_B"]
    elif control[register] == 3:
        registers_next[register] = registers["REG_A"]
    elif control[register] == 4:
        registers_next[register] = registers["RAM_OUT"]
    elif control[register] == 5:
        registers_next[register] = registers["ROM_OUT"]
    elif control[register] == 6:
        registers_next[register] = registers["REG_T"]
    elif control[register] == 7:
        if registers["MA_L"] == 255:
            registers_next["MA_H"] = registers["MA_H"] + 1
            registers_next["MA_L"] = 0
        else:
            registers_next["MA_L"] = registers_next["MA_L"] + 1
    registers_next[register] = registers_next[register] & 255
    registers_next["MEMORY_ADDRESS"] = registers_next["MA_L"] + registers_next["MA_H"] * 256



def t_reg_update():
    if control["REG_T"] == 0:
        pass  # no change
    elif control["REG_T"] == 1:
        registers_next["REG_T"] = registers["REG_A"] + registers["REG_B"]
    elif control["REG_T"] == 2:
        registers_next["REG_T"] = registers["REG_A"] - registers["REG_B"]
    elif control["REG_T"] == 3:
        registers_next["REG_T"] = registers["REG_A"]
    elif control["REG_T"] == 4:
        registers_next["REG_T"] = registers["REG_A"] & registers["REG_B"]
    elif control["REG_T"] == 5:
        registers_next["REG_T"] = registers["REG_A"] | registers["REG_B"]
    elif control["REG_T"] == 6:
        registers_next["REG_T"] = registers["REG_A"] ^ registers["REG_B"]
    elif control["REG_T"] == 7:
        registers_next["REG_T"] = registers["REG_A"] + 1
    elif control["REG_T"] == 8:
        registers_next["REG_T"] = ~registers["REG_T"]
    elif control["REG_T"] == 9:
        registers_next["REG_T"] = registers["REG_T"] + 1
    elif control["REG_T"] == 10:
        registers_next["REG_T"] = registers["REG_T"] - 1
    elif control["REG_T"] == 11:
        pass  # ROTR
    elif control["REG_T"] == 12:
        pass  # ROTL
    elif control["REG_T"] == 13:
        registers_next["REG_T"] = registers["REG_T"] >> 1
    elif control["REG_T"] == 14:
        registers_next["REG_T"] = registers["REG_T"] << 1
    elif control["REG_T"] == 15:
        pass  # no change

    registers_next["REG_T"] = registers_next["REG_T"] & 255

code = {0:{"REG_A": 5, "ROM_OUT": 123}}

def control_update():
    global control_next
    control_next = copy.deepcopy(CONTROL_ZEROS)

    if registers["PROGRAM_COUNTER"] in code:
        for c in code[registers["PROGRAM_COUNTER"]].items():
            control_next[c[0]] = c[1]

    registers_next["ROM_OUT"] = control_next["ROM_OUT"]



for i in range(10):
    pc_update()
    normal_reg_update("REG_A")
    normal_reg_update("REG_B")
    normal_reg_update("PORT")
    normal_reg_update("RAM_IN")
    pc_reg_update("PC_H")
    pc_reg_update("PC_L")
    ma_reg_update("MA_H")
    ma_reg_update("MA_L")
    t_reg_update()

    control_update()
    update()

print(registers)