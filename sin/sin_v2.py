import math

from fxpmath import Fxp
import fxpmath as fp
import random

def mul(a, b):
    return fp.functions.mul(a, b)

ran = random.random()
#print("input:", end=" ")
#print(ran, end="   ")
#print("target:", end=" ")
#print(math.sin(ran*2*math.pi))

FF = Fxp(0x1F, signed=False, n_word=10, n_frac=0)
print("-------")
print(mul(FF,FF+mul(FF, (2**10))).bin())
print("-------")

A = Fxp(ran, signed=False, n_word=6+6, n_frac=6+6)

#print(A.bin(True))

pi = math.pi

print("TT:"+str(math.sin(2*pi*A.get_val())))




def split(fixed_num):
    h = mul(fixed_num, (2**6))
    h = fp.functions.np.floor(h)
    l = mul(fixed_num, (2 ** 6)) - h
    l = mul(l, (2 ** 6))
    l = fp.functions.np.floor(l)

    l = Fxp(l, signed=False, n_word=6, n_frac=0)
    h = Fxp(h, signed=False, n_word=6, n_frac=0)

    return h, l


high, low = split(A)
print("high:"+high.bin())
print("low:"+low.bin())
high = int(high.get_val())
low = int(low.get_val())


h_sin_lut = []
l_sin_lut = []
h_cos_lut = []
l_cos_lut = []
ll_sin_lut = []
ll_cos_lut = []

for i in range(2**6):
    h_sin_lut.append(Fxp(math.sin(i * math.pi * 2 / (2 ** 6)), signed=True, n_word=19, n_frac=18))
    l_sin_lut.append(Fxp(math.sin(i * math.pi * 2 / (2 ** 12)), signed=True, n_word=19, n_frac=18))
    h_cos_lut.append(Fxp(math.cos(i * math.pi * 2 / (2 ** 6)), signed=True, n_word=26, n_frac=25))
    l_cos_lut.append(Fxp(math.cos(i * math.pi * 2 / (2 ** 12)), signed=True, n_word=26, n_frac=25))
    ll_sin_lut.append(Fxp(math.sin(i * math.pi * 2 / (2 ** 18)), signed=True, n_word=19, n_frac=18))
    ll_cos_lut.append(Fxp(math.cos(i * math.pi * 2 / (2 ** 18)), signed=True, n_word=26, n_frac=25))

for i in l_cos_lut:
    print(i.bin())

res = mul(h_sin_lut[high], l_cos_lut[low])+mul(h_cos_lut[high], l_sin_lut[low])
print(res.bin(True))
print(Fxp(math.sin(2*pi*A.get_val()), signed=True, n_word=43, n_frac=42).bin(True))

print(mul(h_sin_lut[high], l_cos_lut[low])+mul(h_cos_lut[high], l_sin_lut[low]))


xx = []
yy = []
tt = []

for i in range(2**12):
    x = i/(2**12)
    xx.append(x)
    tt.append(math.sin(2*pi*x))

    x = Fxp(x, signed=False, n_word=6+6, n_frac=6+6)

    high, low = split(x)
    high = int(high.get_val())
    low = int(low.get_val())

    res = mul(h_sin_lut[high], l_cos_lut[low]) + mul(h_cos_lut[high], l_sin_lut[low])
    yy.append(res)


import matplotlib.pyplot as plt



# plotting the points

gg = []
for i in range(2**12):
    gg.append(Fxp(tt[i]-yy[i], signed=True, n_word=17, n_frac=17).get_val())

plt.plot(xx, gg)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('My first graph!')

# function to show the plot
plt.show()