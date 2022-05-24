import math
import os

import fxpmath.functions
from fxpmath import Fxp
from fxpmath.functions import mul
from fxpmath.functions import np

lut_s_low = []
lut_c_low = []
lut_s_mid = []
lut_c_mid = []
lut_s_high = []
lut_c_high = []

low_size = 0
mid_size = 8
high_size = 8


def split(num):
    num = num << high_size
    high = int(np.floor(num).get_val())
    num = num - high
    num = num << mid_size
    mid = int(np.floor(num).get_val())
    num = num - mid
    num = num << low_size
    low = int(np.floor(num).get_val())
    return high, mid, low


def test(i):
    f_ran = Fxp(i / (2 ** 16), signed=False, n_word=16, n_frac=16)
    h, m, l = split(f_ran)

    left = mul(lut_s_mid[m], lut_c_high[h]) + mul(lut_c_mid[m], lut_s_high[h])
    right = mul(lut_c_mid[m], lut_c_high[h]) - mul(lut_s_mid[m], lut_s_high[h])

    right = mul(lut_s_low[l], right)
    # left = mul(lut_c_low[l], left)
    left = left

    tot = right + left
    target = math.sin(f_ran.get_val() * math.pi * 2)
    target = Fxp(target, signed=True, n_word=17, n_frac=16)

    tot = Fxp(tot, signed=True, n_word=17, n_frac=16)

    if abs(tot - target) <= (2 ** -16):
        # print(tot.bin(True))
        if i % (2 ** 10) == 0:
            print(i)

    else:
        print("-----FAIL----")
        print(abs(tot - target))
        print(target.bin(True))
        print(tot.bin(True))
        print("-------------")

    pass


from multiprocessing import Pool

for i in range(2 ** low_size):
    s = Fxp(math.sin(i * 2 * math.pi / (2 ** 16)), signed=False, n_word=9, n_frac=18)
    c = Fxp(math.cos(i * 2 * math.pi / (2 ** 16)), signed=False, n_word=19, n_frac=18)
    s = np.floor(s << 18) >> 18
    c = np.floor(c << 18) >> 18
    lut_s_low.append(Fxp(s, False, 9, 18))
    lut_c_low.append(Fxp(1, False, 19, 18))


for i in range(2 ** mid_size):
    s = Fxp(math.sin(i * 2 * math.pi / (2 ** (16 - low_size))), signed=False, n_word=15, n_frac=18)
    c = Fxp(math.cos(i * 2 * math.pi / (2 ** (16 - low_size))), signed=False, n_word=18, n_frac=18)
    s = np.floor(s << 18) >> 18
    c = np.floor(c << 17) >> 17
    lut_s_mid.append(Fxp(s, False, 13, 18))
    lut_c_mid.append(Fxp(c, False, 18, 18))


for i in range(2 ** high_size):
    s = Fxp(math.sin(i * 2 * math.pi / (2 ** (16 - low_size - mid_size))), signed=True, n_word=19, n_frac=18)
    c = Fxp(math.cos(i * 2 * math.pi / (2 ** (16 - low_size - mid_size))), signed=True, n_word=15, n_frac=14)
    s = np.floor(s << 18) >> 18
    c = np.floor(c << 14) >> 14
    lut_s_high.append(Fxp(s, True, 19, 18))
    lut_c_high.append(Fxp(c, True, 15, 14))

if __name__ == '__main__':

    # 4 6 6 configuration
    # lut_s_low 10 data bits
    # lut_c_low 3 data bits
    # lut_s_mid 17 data bits
    # lut_c_mid 15 data bits
    # lut_s_high 19 data bits
    # lut_c_high 19 data bits

    # 4 5 7 configuration
    # lut_s_low 12 data bits
    # lut_c_low 5 data bits
    # lut_s_mid 17 data bits
    # lut_c_mid 15 data bits
    # lut_s_high 19 data bits
    # lut_c_high 19 data bits

    # 6 4 6 configuration
    # lut_s_low 10 data bits
    # lut_c_low 3 data bits
    # lut_s_mid 15 data bits
    # lut_c_mid 11 data bits
    # lut_s_high 19 data bits
    # lut_c_high 19 data bits

    # 6 5 5 configuration
    # lut_s_low 10 data bits
    # lut_c_low 1 data bits
    # lut_s_mid 15 data bits
    # lut_c_mid 11 data bits
    # lut_s_high 19 data bits
    # lut_c_high 19 data bits

    # 6 6 4 configuration
    # lut_s_low 9 data bits
    # lut_c_low 0 data bits
    # lut_s_mid 15 data bits
    # lut_c_mid 11 data bits
    # lut_s_high 19 data bits
    # lut_c_high 15 data bits

    # 8 8 0 configuration
    # lut_s_low 0 data bits
    # lut_c_low 0 data bits
    # lut_s_mid 13 data bits
    # lut_c_mid 7 data bits
    # lut_s_high 19 data bits
    # lut_c_high 15 data bits

    if False:
        for i in range(8):
            print("in_"+str(i),end=",")
        for i in range(13):
            print("out_"+str(i),end=",")
        print()
        for idx, i in enumerate(lut_s_mid):
            print(str(Fxp(idx,False,8).bin())+str(i.bin()))

    for idx, i in enumerate(lut_s_low):
        print(i.bin(True))


    with Pool(os.cpu_count() - 1) as p:
        result = p.map(test, range(2 ** 16))
