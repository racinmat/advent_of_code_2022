import time
from os.path import dirname
from pathlib import Path
from misc import read_day, submit_day, prettytime
import numpy as np


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()
    shapes_txt = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##\
"""
    shapes = []
    for s_text in shapes_txt.split('\n\n'):
        lines = s_text.split('\n')
        shape = np.zeros((len(lines), len(lines[0])), dtype=np.bool)
        for i, l in enumerate(lines):
            shape[i, [j == '#' for j in l]] = 1
        shapes.append(shape)

    # grid = np.zeros((100_000, 7))
    grid = np.zeros((20, 7), dtype=np.bool)
    depth, tot_width = grid.shape
    for i in range(2022):
        shape = shapes[i % len(shapes)]
        x, y = shape.shape
        width = 2
        if np.all(grid == 0):
            height = 3
        else:
            height = np.argmax(np.argmax(grid, axis=1), axis=0) + 3
        height = depth - height
        j = -1
        while True:
            copy_grid = np.copy(grid)
            j += 1
            p = pattern[j]
            copy_grid[height - x:height, width:(width + y)] += shape
            if p == '>':
                width = min(width + 1, tot_width - x)
            else:
                width = max(width - 1, 0)
            height += 1
            copy_grid[height - x:height, width:(width + y)] += shape
            if np.any(copy_grid > 1):
                break


def execute_part2():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')


if __name__ == '__main__':
    read_day(17)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 17, 1)
    # submit_day(res2, 17, 2)
    print(f"day 17 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 17 part 2 in {prettytime(toc - tac)}, answer: {res2}")
