import numpy as np
import scipy.sparse

directions = {"L": (1, -1), "R": (1, 1), "D": (0, -1), "U": (0, 1)}


def draw(origin, line):
    current = origin[:]
    grid = scipy.sparse.lil_matrix((20000, 20000), dtype=np.int32)
    count = 0

    for move in line:
        direction = move[0]
        distance = int(move[1:])

        idx, inc = directions[direction]

        while distance > 0:

            distance -= 1
            count += 1
            current[idx] += inc

            if min(current) < 0 or max(current) > grid.shape[0]:
                raise ValueError("gone off the board: {}".format(current))

            if grid[current[0], current[1]] == 0:
                grid[current[0], current[1]] = count

    return grid


with open("003.txt", "r") as f:
    line_a = f.readline().strip().split(",")
    line_b = f.readline().strip().split(",")

origin = [5000, 5000]

print("grids")
grid_a = draw(origin, line_a)
grid_b = draw(origin, line_b)

print("sums")
grid = grid_a + grid_b
grid_mask = (grid_a > 0).astype(int) + (grid_b > 0).astype(int)

print("intersection")
intersections = grid[grid_mask == 2]
print("smallest", np.min(intersections))


"""
# from scipy.spatial import distance
distances = []
for i in intersections:
    if np.all(i == origin[0]):
        continue
    distances.append([i, distance.cityblock(origin, i)])
    print(distances[-1])

smallest = list(sorted(distances, key=lambda x: x[1]))[0]
"""
