import numpy as np
import math

def vision(asteroids, x, y):
    angles = [
        math.atan2(y - y1, x - x1) * 180 / math.pi
        for x1, y1 in asteroids
    ]

    return len(np.unique(angles, axis=0) - 1)


with open("010.txt", "r") as f:
    grid = np.array([list(fi) for fi in f.read().split("\n")[:-1]])

asteroids = np.argwhere(grid=='#')
print(max([vision(asteroids, x, y) for x, y in asteroids]))
