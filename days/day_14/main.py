import time
from os.path import dirname
from pathlib import Path

from scipy.sparse import coo_array

from misc import read_day, submit_day, prettytime
import numpy as np

# it's both the same, we don't need to distinguish between them
ROCK = 1
SAND = 1


def build_grid(data, wide_grid=False):
    rocks = [[list(map(int, i.split(','))) for i in l.split(' -> ')] for l in data]
    x_max = max(j[1] for i in rocks for j in i) + 1
    y_max = max(j[0] for i in rocks for j in i) + 1
    # numpy does not have native bit matrices
    # grid = coo_array((x_max, y_max), dtype=np.byte)
    grid = np.zeros((x_max + 2 if wide_grid else x_max, max(y_max, 500+2+x_max+1) if wide_grid else y_max), dtype=np.byte)
    for shape in rocks:
        for (y1, x1), (y2, x2) in zip(shape[:-1], shape[1:]):
            y_from = min(y1, y2)
            y_to = max(y1, y2)
            x_from = min(x1, x2)
            x_to = max(x1, x2)
            grid[x_from:x_to + 1, y_from:y_to + 1] = ROCK
    return grid


def simulate_sand(grid):
    infinite_fall = False
    y_start = 500
    i = -1
    while not infinite_fall:
        i += 1
        new_x, new_y = 0, y_start
        falling = True
        while falling:
            grounds = np.where(grid[new_x:, new_y])[0]
            if len(grounds) > 0:
                x_ground = grounds[0]
            else:
                infinite_fall = True
                break
            new_x, new_y = new_x + x_ground - 1, new_y
            # look left down
            if not grid[new_x + 1, new_y - 1]:
                new_x, new_y = new_x + 1, new_y - 1
            elif not grid[new_x + 1, new_y + 1]:
                new_x, new_y = new_x + 1, new_y + 1
            else:
                falling = False
        grid[new_x, new_y] = SAND
        if (new_x, new_y) == (0, y_start):
            infinite_fall = True
            break
    return i


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    grid = build_grid(data)
    i = simulate_sand(grid)
    return i


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    grid = build_grid(data, wide_grid=True)
    grid[-1, :] = ROCK
    i = simulate_sand(grid)
    return i + 1


if __name__ == '__main__':
    read_day(14)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 14, 1)
    # submit_day(res2, 14, 2)
    print(f"day 14 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 14 part 2 in {prettytime(toc - tac)}, answer: {res2}")
# there is space for optimization, definitely
# day 14 part 1 in 78.322 ms, answer: 618
# day 14 part 2 in 5.404 s, answer: 26358
