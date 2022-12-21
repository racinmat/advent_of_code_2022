import time
from os.path import dirname
from pathlib import Path
from days.day_17 import my_module
from misc import read_day, submit_day, prettytime
import numpy as np
from statsmodels import api as sm
import matplotlib.pyplot as plt


def check_period(arr, n):
    a = np.split(arr, np.arange(n, len(arr), n))
    return [j - i for i, j in zip(a[:-1], a[1:]) if len(i) == len(j)]


def prepare_shapes():
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
    return shapes


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()
    shapes = prepare_shapes()
    depth = 6_000
    # depth = 30
    grid, _, _ = my_module.simulate_tetris(pattern, shapes, depth, 2022)
    return int(depth - np.argmax(np.max(grid, axis=1), axis=0))


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()
    shapes = prepare_shapes()
    depth = 25_000
    # guessing that I will find period after sim_steps
    sim_steps = 5_000
    target_steps = 1_000_000_000_000
    # target_steps = 2022
    grid, blocks, heights = my_module.simulate_tetris(pattern, shapes, depth, sim_steps)

    hn_lags = min(5_000, len(heights) - 1)
    hacf = sm.tsa.acf(heights, nlags=hn_lags)  # guess how much to compute

    hperiod = np.argsort(hacf)[::-1][1]
    # for test data, it's 53 period and offset 25

    hoffset = 0
    for j in range(hperiod):
        a1 = check_period(heights[j:], hperiod)
        if np.all(list(map(lambda x: x == 0, a1[:30]))):
            hoffset = j
            break

    offset_num = hoffset + 1
    cur_height = np.sum(heights[:hoffset])
    period_height = np.sum(heights[:hoffset + hperiod]) - np.sum(heights[:hoffset])
    cur_blocks = hoffset
    num_periods = (target_steps - offset_num) // hperiod
    cur_height += num_periods * period_height
    cur_blocks += num_periods * hperiod
    # add the part of period
    remaining_blocks = target_steps - cur_blocks
    cur_height += np.sum(heights[hoffset:hoffset + remaining_blocks])
    cur_blocks += remaining_blocks
    return int(cur_height)


if __name__ == '__main__':
    read_day(17)
    tic = time.perf_counter()
    res1 = execute_part1()
    print('done day 1')
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 17, 1)
    # submit_day(res2, 17, 2)
    print(f"day 17 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 17 part 2 in {prettytime(toc - tac)}, answer: {res2}")
