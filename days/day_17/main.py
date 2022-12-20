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
        shape = np.zeros((len(lines), len(lines[0])), dtype=bool)
        for i, l in enumerate(lines):
            shape[i, [j == '#' for j in l]] = 1
        shapes.append(shape)

    # grid = np.zeros((5_000, 7), dtype=np.int8)
    grid = np.zeros((30, 7), dtype=np.int8)
    depth, tot_width = grid.shape
    j = -1
    for i in range(2022):
        shape = shapes[i % len(shapes)]
        height, width = shape.shape
        x = 2
        if np.all(grid == 0):
            y = depth - 3
        else:
            y = np.argmax(np.max(grid, axis=1), axis=0) - 3
        print(f'starts falling: {x=}, {y=}')
        even = False
        while True:
            copy_grid = np.copy(grid)
            old_x, old_y = x, y
            if even:
                y += 1
                print(f'falls down')
            else:
                j += 1
                j %= len(pattern)
                p = pattern[j]
                if p == '>':
                    # todo: add here the test for not being pushed towards stone
                    x = min(x + 1, tot_width - width)
                    print(f'pushes right{", nothing happens" if x == tot_width - width else ""}, {x=}, {y=}')
                else:
                    x = max(x - 1, 0)
                    print(f'pushes left{", nothing happens" if x == 0 else ""}, {x=}, {y=}')
            copy_grid[y - height:y, x:x + width] += shape
            even = not even
            # todo: if sth should be pushed towards other stone but can fall down, I should continue and now push it
            if np.any(copy_grid > 1) or y > depth:
                break
        grid[old_y - height:old_y, old_x:old_x + width] += shape

    print('')
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
