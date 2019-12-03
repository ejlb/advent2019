import numpy as np


def draw(origin, line):
    current = origin[:]
    grid = np.zeros((20000, 20000))
    count = 0

    for move in line:
        direction = move[0]
        distance = int(move[1:])

        while distance > 0:
            distance -= 1
            count += 1

            if direction == "L":
                current[1] -= 1
            elif direction == "R":
                current[1] += 1
            elif direction == "U":
                current[0] += 1
            elif direction == "D":
                current[0] -= 1
            else:
                raise ValueError("invalid direction {}".format(move))

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
print("sum")
grid = grid_a + grid_b

print("intersec")
intersections = grid[np.logical_and(grid > 0, np.logical_and(grid_a != 0, grid_b != 0))]
print("smallest", np.sort(intersections).astype(int)[0])


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
