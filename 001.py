import numpy as np

s = 0

for i in open('001.txt', 'r').read().strip().split('\n'):
    fuel = np.floor(float(i) / 3) - 2

    while fuel > 0:
        s += fuel
        fuel = np.floor(float(fuel) / 3) - 2

print(s)
