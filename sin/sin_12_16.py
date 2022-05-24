import math
import os

import fxpmath.functions
from fxpmath import Fxp
from fxpmath.functions import mul
from fxpmath.functions import np

lut_s_low = []
lut_c_low = []
lut_s_high = []
lut_c_high = []



CONFIG_8_4 = {"low_size": 4,
              "high_size": 8,
              "s_low_nword": 21,
              "s_low_nfrac": 26,
              "c_low_nword": 26,
              "c_low_nfrac": 25,

              "s_high_nword": 28,
              "s_high_nfrac": 27,
              "c_high_nword": 23,
              "c_high_nfrac": 22,
              }

# N.11111111111NNNNNNNNNNNNNN lut_c_low 15 bits data, 26 bit mult :(
#  .00000NNNNNNNNNNNNNNNNNNNNN lut_s_low 21 bits data, 21 bit mult
# 1.111110011011011110101010101 lut_s_high 28 bits dat, 28 bit mult
# 1.1111100110110111101011  lut_c_high 23 bits dat, 23 bit mult
CONFIG_6_6 = {"low_size": 6,
              "high_size": 6,
              "s_low_nword": 25,
              "s_low_nfrac": 28,
              "c_low_nword": 27,
              "c_low_nfrac": 26,

              "s_high_nword": 28,
              "s_high_nfrac": 27,
              "c_high_nword": 22,
              "c_high_nfrac": 21,
              }

CONFIG_5_5 = {"low_size": 5,
              "high_size": 5,
              "s_low_nword": 26,
              "s_low_nfrac": 26,
              "c_low_nword": 31,
              "c_low_nfrac": 30,

              "s_high_nword": 31,
              "s_high_nfrac": 30,
              "c_high_nword": 31,
              "c_high_nfrac": 30,
              }

conf = CONFIG_5_5
low_size = conf["low_size"]
high_size = conf["high_size"]


def split(num):
    num = num << high_size
    high = int(np.floor(num).get_val())
    num = num - high
    num = num << low_size
    low = int(np.floor(num).get_val())
    return high, low


for i in range(2 ** low_size):
    s = Fxp(math.sin((i / 2) * math.pi / (2 ** 10)), False, conf["s_low_nword"], conf["s_low_nfrac"])
    c = Fxp(math.cos((i / 2) * math.pi / (2 ** 10)), False, conf["c_low_nword"], conf["c_low_nfrac"])
    lut_s_low.append(s)
    lut_c_low.append(c)

for i in range(2 ** high_size):
    s = Fxp(math.sin((i / 2) * math.pi / (2 ** (10 - low_size))), False, conf["s_high_nword"], conf["s_high_nfrac"])
    c = Fxp(math.cos((i / 2) * math.pi / (2 ** (10 - low_size))), False, conf["c_high_nword"], conf["c_high_nfrac"])
    lut_s_high.append(s)
    lut_c_high.append(c)


def test(i):
    f_ran = Fxp(i / (2 ** 10), signed=False, n_word=12, n_frac=12)
    h, l = split(f_ran)

    tot = mul(lut_s_low[l], lut_c_high[h]) + mul(lut_c_low[l], lut_s_high[h])

    target = math.sin(f_ran.get_val() * math.pi/2)
    target = Fxp(target, signed=True, n_word=17, n_frac=16)
    tot = Fxp(tot, signed=True, n_word=17, n_frac=16)

    if abs(tot - target) == 0:
        # print(tot.bin(True))
        if i % (2 ** 10) == 0:
            print(i)

    else:
        print("-----FAIL----")
        print("indices - h:" + str(h) + "   L:" + str(l))
        print("H sin:" + lut_s_high[h].bin(True))
        print("H cos:" + lut_c_high[h].bin(True))
        print("L sin:" + lut_s_low[l].bin(True))
        print("L cos:" + lut_c_low[l].bin(True))
        print(abs(tot - target))
        print(target.bin(True))
        print(tot.bin(True))
        print("-------------")

    pass


from multiprocessing import Pool

if __name__ == '__main__':

    for i in lut_c_low:
        print(i.bin(True))

    with Pool(os.cpu_count() - 1) as p:
        result = p.map(test, range(2 ** 10))
