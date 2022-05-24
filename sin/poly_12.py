import math
import os

import fxpmath.functions
from fxpmath import Fxp
from fxpmath.functions import mul
from fxpmath.functions import np
from math import pi

#f(H+L) = f(H)+f'(H)*L+c(H,L)

SEL_BITS = 2-1
H_BITS = 7
L_BITS = 3

f_lut = []
f_prime_lut = []

for i in range(2 ** (H_BITS+2)):
    # 0->0
    # 2 ** H_BITS -> 1

    f = Fxp(math.sin((i / 2) * math.pi / (2 ** H_BITS)), False, 15, 15)
    f_prime = Fxp(2*math.pi*(math.cos((i / 2) * math.pi / (2 ** H_BITS))), False, 15, 10)
    f_lut.append(f)
    f_prime_lut.append(f_prime)


def split(num):
    num = num << SEL_BITS
    s = np.floor(num)
    num = num - s
    num = num << H_BITS
    h = np.floor(num)
    num = num - h
    num = num << L_BITS
    l = np.floor(num)

    return s, h, l


def approx(high,low):
    # f(H+L) = f(H)+f'(H)*L+c(H,L)
    f0 = f_lut[high]
    f1 = f_prime_lut[high]

    return f0+f1*low

    #f_lut[high]+

def test(num):
    num = Fxp(num, False, 12, 11)
    sel, high, low = split(num)
    sel = int(sel)
    high = int(high)
    low = low >> (L_BITS+SEL_BITS+H_BITS)

    target = math.sin(pi*num.get_val())
    target = Fxp(target, True, 16, 15)
    print()
    print("INPUT:"+str(num))
    print("TARGET:" + str(target))
    res = approx(high, low)
    err = Fxp(target-res, True, 16, 15)
    print("RESULT:" + str(res))
    print("ERROR:"+err.bin(True))
    print()


for i in range(2**(H_BITS+L_BITS)):
    i = i/4
    i = i/(2**(H_BITS+L_BITS))
    test(i)


