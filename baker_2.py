import random
import multiprocessing as mp
import numpy as np

# import cupy as np


LENGTH = 300


def self_conv(pulse, noise=0):
    conv = np.convolve(np.flip(pulse, 0), pulse)
    return conv + rand_list(conv.size, noise)


def rand_list(length, scale=1):
    return (np.random.rand(length) - 0.5) * 2 * scale


def gain(pulse):
    p = pulse.flatten()
    p = np.abs(p)
    p.sort()
    return p[-1]**2 / p[-4]


def optimize(pulse):
    p = np.copy(pulse) + rand_list(len(pulse), 0.001)
    p = np.clip(p, -1, 1)
    old_score = gain(self_conv(pulse, 0.01))
    new_score = gain(self_conv(p, 0.01))

    if new_score > old_score:
        return new_score, p
    return old_score, pulse


def first_guess(pulse_len):
    best_pulse = []
    best_gain = -9999999999999

    for i in range(10000):
        if i % 200 == 0:
            print(i)
        pulse = rand_list(pulse_len)
        aaa = self_conv(pulse, 0.01)
        l_gain = gain(aaa)
        if l_gain > best_gain:
            print(best_gain)
            best_gain = l_gain
            best_pulse = pulse

    for i in range(100000):
        if i % 567 == 0:
            print(i)
        best_gain, best_pulse = optimize(best_pulse)

    return best_gain, best_pulse


def print_pulse(pulse):
    print(str(pulse.tolist()).replace("[", "").replace("]", "").replace(",", "").replace(".", ","))


if __name__ == '__main__':

    pool = mp.Pool(mp.cpu_count() - 1)

    results = pool.map(first_guess, [2000] * (mp.cpu_count() - 1))

    pool.close()

    best_gain = 0
    best_pulse = None
    for r in results:
        l_gain = gain(self_conv(r[1]))
        if l_gain > best_gain:
            best_gain = l_gain
            best_pulse = r[1]

    print_pulse(best_pulse)
    print_pulse(self_conv(best_pulse))

    # print_pulse(results)
