
import fxpmath.functions
import math

from fxpmath import Fxp
from fxpmath.functions import mul
from fxpmath.functions import np

xx = []
for i in range(2**10):
    xx.append(i/(2**10))

aa = []
bb = []
for i in range(2**18):
    aa.append(-0.5+i/(2**18))
    bb.append(-0.5 + i / (2 ** 18))

best = 9999999999999999999999999999999

for a in range(2**10):
    a = ((-0.5+a)*10)/(2**10)
    for b in range(2**11):
        b = ((-0.5+a)*10)/(2**11)

        ab_error = 0
        for x in xx:
            target = math.sin(x * math.pi / 2)
            local_error = math.floor((2 ** 16)*(target-b+a*x+x**2))/(2 ** 16)
            ab_error += local_error
        if ab_error < best:
            best = ab_error
            print("...........")
            print("A:"+str(a))
            print("B:"+str(b))

            pass
