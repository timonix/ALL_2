import math

h_sin_lut = dict()
l_sin_lut = dict()
h_cos_lut = dict()
l_cos_lut = dict()

for i in range(2**12):
    h_sin_lut[i] = math.sin(i)
    l_sin_lut[i] = math.sin(i/(2**12))
    h_cos_lut[i] = math.cos(i)
    l_cos_lut[i] = math.cos(i / (2 ** 12))

def split(float_num):
    high = math.floor(float_num)
    low = (float_num-high)*(2**12)
    low = math.floor(low)
    return high, low

def my_sin(float_num):
    high, low = split(float_num)
    return h_sin_lut[high]*l_cos_lut[low]+h_cos_lut[high]*l_sin_lut[low]


import numpy as np
import matplotlib.pyplot as plot


time = np.arange(0, 0.125/2+0.125/4+0.125/8+0.125/16, 1/(2**12))

amplitude = np.sin(time)

amplitude2 = []
def quant_sin(float_num):
    q = math.sin(float_num)
    q = quant(q)
    return q

def quant(floatnum):
    q = floatnum * (2 ** 12)
    q = math.floor(q)
    q = q / (2 ** 12)
    return q

for t in time:

    amplitude2.append(quant_sin(t)-quant(t)+1/(2**12))

plot.plot(time, amplitude2)

plot.title('Sine wave')

plot.xlabel('Time')

plot.ylabel('Amplitude = sin(time)')

plot.grid(True, which='both')

plot.axhline(y=0, color='k')

plot.show()

# Display the sine wave

plot.show()

