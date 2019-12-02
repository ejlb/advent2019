import numpy as np

s = 0

for i in open('001.txt', 'r').read().strip().split('\n'):
    fule = np.floor(float(i) / 3) - 2

    while fule > 0:
        s += fule
        fule = np.floor(float(fule) / 3) - 2

print(s)
