import numpy as np
import math

def vision(asteroids, x, y):
    angles = [
        math.atan2(y - y1, x - x1) * 180 / math.pi
        for x1, y1 in asteroids
    ]

    return len(np.unique(angles, axis=0) - 1)


def rotate(x, y, angle):
    """Use numpy to build a rotation matrix and take the dot product."""
    radians = angle * math.pi / 180
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return float(m.T[0]), float(m.T[1])


def distance(a,b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


def is_between(a,c,b):
    return distance(a,c) + distance(c,b) == distance(a,b)


with open("010.txt", "r") as f:
    grid = np.array([list(fi) for fi in f.read().split("\n")[:-1]])

asteroids = np.argwhere(grid=='#')
vision_count = [[(x, y), vision(asteroids, x, y)] for x, y in asteroids]
best = sorted(vision_count, key=lambda x: x[1])[-1][0]

print('best', best)

for angle in range(0, 361):
    print(angle, rotate(best[0], best[1], angle))

