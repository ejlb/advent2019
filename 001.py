import numpy as np


s = 0
for i in open('001.txt', 'r').read().split('\n'):
    if not i:
        continue

    fule = np.floor(float(i) / 3)- 2
    while fule > 0:
        s+= fule
        fule = np.floor(float(fule) / 3)- 2

print(s)


#divide by three, round down, and subtract 2.
