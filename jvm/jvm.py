from OPCODES import *


def executeMethod(code, constant_pool, stack, stackPtrStart):
    variables = [None]*10
    sp = stackPtrStart
    pc = 0
    done = False
    while not done:
        if pc >= len(code):
            done = True
        elif code[pc] == ICONST_1:
            stack[sp] = 1
            sp += 1
            pc += 1
        elif code[pc] == IADD:
            stack[sp - 2] = stack[sp - 1] + stack[sp - 2]
            sp += -2
            pc += 1
        elif code[pc] == IRETURN:
            stack[stackPtrStart] = stack[sp]
            done = True
        elif code[pc] == BIPUSH:
            stack[sp] = code[pc+1]
            sp += 1
            pc += 2
        elif code[pc] == BIPUSH:
            stack[sp] = code[pc+1]
            sp += 1
            pc += 2
        elif code[pc] == ISTORE_1:
            variables[1] = stack[sp-1]
            sp += -1
            pc += 1
        elif code[pc] == ISTORE_2:
            variables[2] = stack[sp-1]
            sp += -1
            pc += 1
        elif code[pc] == ILOAD_1:
            stack[sp] = variables[1]
            pc += 1
        elif code[pc] == ILOAD_2:
            stack[sp] = variables[2]
            sp += 1
            pc += 1

        else:
            done = True
            print("ILLEGAL INSTRUCTION:"+str(hex(code[pc])))

