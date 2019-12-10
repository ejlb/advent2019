import numpy as np
import math


def vision(grid, x, y):
    angles = []

    for y1 in range(grid.shape[0]):
        for x1 in range(grid.shape[1]):
            if grid[x1][y1] == "#":
                if x == x1 and y == y1:
                    continue
                angles.append(math.atan2(y - y1, x - x1) * 180 / math.pi)

    return len(np.unique(angles, axis=0) - 1)


with open("010.txt", "r") as f:
    grid = np.array([list(fi) for fi in f.read().split("\n")[:-1]])
    print(grid)

vision_count = []
count = 0

for y in range(grid.shape[0]):
    for x in range(grid.shape[1]):
        if grid[x][y] == "#":
            vision_count.append([(x, y), vision(grid, x, y)])
            count += 1

print("test {} astroids".format(count))

for i in sorted(vision_count, key=lambda x: x[1]):
    print(i)
