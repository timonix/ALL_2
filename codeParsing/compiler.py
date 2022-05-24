import re


def floatToBinary(data):
    tmp = float(data)
    tmp = tmp * (2 ** 12)  # shift everything left.
    return int(round(tmp))  # remove everything beyond the dot


def longToBinaryHigh(data):
    tmp = data >> 24
    return tmp


def longToBinaryLow(data):
    tmp = data & 0xFFFFFF
    return tmp


def doubleToBinaryHigh(data):
    tmp = float(data)
    tmp = tmp * (2 ** 24)
    tmp = int(round(tmp))
    tmp = tmp >> 24
    return tmp


def doubleToBinaryLow(data):
    tmp = float(data)
    tmp = tmp * (2 ** 24)
    tmp = int(round(tmp))
    tmp = tmp & 0xFFFFFF
    return tmp


def assembly_from_function(function_dict, constant_dict, memory):
    print(function_dict)
    print(constant_dict)
    print(memory)
    print("...........")
    for fun in function_dict.items():
        fun_code = []
        local_varaibles = {}
        for c in fun[1]["code"]:  # count variables
            if c.startswith("return"):  #
                pass
            else:
                var = re.findall(r'\w*(?=\=)', c)
                var = [x for x in var if x]
                if var[0] not in constant_dict and var[0] not in local_varaibles:
                    local_varaibles[var] =





def machine_code_from_constants(constant_dict):
    index_counter = 1
    machine_code = []

    for variable in constant_dict.items():
        data_type = variable[1]["type"]
        data = variable[1]["value"]
        if data_type == "i":
            variable[1]["location"] = index_counter
            index_counter += 1
            machine_code.append(int(data))
        if data_type == "f":
            variable[1]["location"] = index_counter
            index_counter += 1
            machine_code.append(floatToBinary(data))
        if data_type == "l":
            variable[1]["location"] = index_counter
            index_counter += 2
            machine_code.append(longToBinaryHigh(data))
            machine_code.append(longToBinaryLow(data))
        if data_type == "d":
            variable[1]["location"] = index_counter
            index_counter += 2
            machine_code.append(doubleToBinaryHigh(data))
            machine_code.append(doubleToBinaryLow(data))
        if data_type == "F":
            variable[1]["location"] = index_counter
            index_counter += len(data)
            for d in data:
                machine_code.append(floatToBinary(d))
        if data_type == "D":
            variable[1]["location"] = index_counter
            index_counter += len(data)
            for d in data:
                machine_code.append(doubleToBinaryHigh(d))
                machine_code.append(doubleToBinaryLow(d))
        if data_type == "A":
            variable[1]["location"] = index_counter
            index_counter += int(data)
            for d in range(int(data)):
                machine_code.append(0)

    return constant_dict, machine_code
