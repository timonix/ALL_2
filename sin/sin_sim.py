import math

from fxpmath import Fxp



lut_s = []
lut_c = []

# X.HHH HHH LLLL LLLL LLLL LLLL LL


for i in range(25):
    print("O"+str(i),end=",")

for i in range(2**6):
    lut_s.append(Fxp(math.sin(i*2*math.pi/(2**6)), signed=True, n_word=18+25+1, n_frac=18+25))
    lut_c.append(Fxp(math.cos(i*2*math.pi/(2**6)), signed=True, n_word=25+1, n_frac=16))

print(math.cos(0*2*math.pi/(2**6)))
for input, c in enumerate(lut_s):
    print(Fxp(input, signed=False, n_word=6).bin(),end="")
    print(c.bin())
print(lut_c[32])
