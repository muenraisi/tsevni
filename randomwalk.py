import numpy as np
import matplotlib.pyplot as plt
import random
import math as math




def simple_random_walk():
    N = 1000
    value = 1
    x = np.arange(0, N)
    y = [0]
    z = [10]
    momentum = 0
    delta = 0
    rational = 0.0001
    power = 0.0001
    for i in range(1, N):
        if len(y) > 11:
            momentum = y[i - 1] - y[i - 11]
        else:
            momentum = 0
        delta = random.gauss(0,.03333)
        # if delta >0.1:
        #     delta=0.1
        # elif delta<-0.1:
        #     delta=-0.1
        # else:
        #     pass

        if y[-1] >= value:
            rational = rational * 0.999
            if rational < 1e-8:
                rational = 1e-8
            rise = delta
        else:
            rational = rational * 1.001
            if rational > 0.8:
                rational = 0.8
            rise = delta
        y.append(y[-1] +rise)
        # y.append(y[-1]+delta*0.1+momentum*0.06)
        # z.append(z[-1] + delta * 0.1 )

    # plt.plot(x, y)
    # plt.yscale('log')
    #
    #
    # plt.show()
    return y[-1]

res=[]
P=1.
for i in range(1000):
    r=simple_random_walk()
    print(i,r)
    res.append(r)
    P=P*r
print(np.mean(res))