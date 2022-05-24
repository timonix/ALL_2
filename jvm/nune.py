Op_codes = {
    0x03: "iconst_0",
    0x3b: "istore_0",
    0x84: "iinc",  # Two arguments
    0x1a: "iload_0",
    0x05: "iconst_2",
    0x68: "imul",
    0x3b: "istore_0",
}

code = [0x03, 0x3b, 0x84, 0x00, 0x01, 0x1a, 0x05, 0x68, 0x3b, 0xa7, 0xff, 0xf9]

NUMBER_OF_REGISTERS = 10

main = []
fun = []

stack = []
variables = [None] * NUMBER_OF_REGISTERS
constant_pool = [main, fun]

pc = 0


def getOffset(pc):
    branchbyte1 = code[pc + 1]
    branchbyte2 = code[pc + 2]
    offset = branchbyte1 << 8 | branchbyte2
    if offset & 0x8000 == 0x8000:
        offset = -(-offset & 0xFFFF)

    return offset - 1


verbose = False
while pc < len(code):
    if verbose:
        print(Op_codes[code[pc]], end = ' ')
    if code[pc] == 0x03:  # iconst_0
        stack.append(0)
    elif code[pc] == 0x05:  # iconst_2
        stack.append(2)
    elif code[pc] == 0x3b:  # istore_0
        variables[0] = stack.pop()
    elif code[pc] == 0x84:  # iinc takes two arguments
        if verbose:
            print(code[pc + 1], end=' ')
            print(code[pc + 2], end=' ')
        variables[code[pc + 1]] = variables[code[pc + 1]] + code[pc + 2]
        pc = pc + 2
    elif code[pc] == 0x1a:  # iload_0
        stack.append(variables[0])
    elif code[pc] == 0x68:  # imul
        stack.append(stack.pop() * stack.pop())
    elif code[pc] == 0xa7:  # goto takes two arguments
        pc = pc + getOffset(pc)
    elif code[pc] == 0x9f:  # if_icmpeq, if ints are equal, branch
        if stack.pop() == stack.pop():
            pc = pc + getOffset(pc)
    elif code[pc] == 0x60:  # iadd
        stack.append(stack.pop() + stack.pop())
    elif code[pc] == 0x80:  # ior
        stack.append(stack.pop() | stack.pop())
    elif code[pc] == 0x70:  # irem
        stack.append(stack.pop() % stack.pop())
    elif code[pc] == 0xb7:  # invokespecial
        stack.append(pc + 2)
        code = constant_pool[getOffset(pc)]
        pc = -1

        # invoke instance method on object objectref and puts the result on the stack (might be void);
        # the method is identified by method reference index in constant pool (indexbyte1 << 8 | indexbyte2)
    else:
        print("illegal operation:" + str(code[pc]))
    if verbose:
        print()
    pc = pc + 1
