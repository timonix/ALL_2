import math
import multiprocessing
import random
import copy

from multiprocessing import Pool


def thread():
    best = -999999999
    best_sig = []
    best_ret = []

    for i in range(10000):
        signal = []
        for j in range(0, 2000):
            n = random.uniform(-1, 1)
            signal.append(n)

        return_signal = [0] * len(signal)
        return_signal.extend(signal)
        return_signal.extend([0] * (len(signal) + 1))

        resp = []
        for i in range(len(return_signal) - len(signal)):

            sum = 0
            for j in range(len(signal)):
                sum += signal[j] * return_signal[i + j]
            resp.append(sum)

        c = copy.copy(resp)
        c = [abs(number) for number in c]
        c.sort()
        score = c[-1]/c[-2]

        if score > best:
            best_sig = signal
            best_ret = resp
            best = score
            print(best)
    if best > -999999999:
        print(best)
        #print(str(best_sig).replace("[", "").replace("]", "").replace(",", "").replace(".", ","))


if __name__ == '__main__':
    for i in range(4):
        p2 = multiprocessing.Process(target=thread, args=())
        p2.start()
