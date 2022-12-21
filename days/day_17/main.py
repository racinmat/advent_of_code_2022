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


def simulate_tetris(pattern, shapes, depth, n_steps):
    grid = np.zeros((depth, 7), dtype=np.int8)
    grid2 = np.zeros((depth, 7), dtype=np.int64)
    blocks = - np.ones(depth, dtype=np.int32)
    heights = np.zeros(n_steps, dtype=np.int8)
    tot_width = grid.shape[1]
    j = -1
    old_height = depth
    max_height = depth
    for i in range(n_steps):
        shape = shapes[i % len(shapes)]
        height, width = shape.shape
        x = 2
        if np.all(grid == 0):
            y = depth - 3
        else:
            max_line = np.count_nonzero(grid, 1) > 0
            y = np.argmax(max_line, 0) - 3
        # print(f'{i}th starts falling: {x=},{y=}')
        even = False
        hit_floor = False
        while True:
            old_x, old_y = x, y
            if even:
                y += 1
                # print(f'falls down to {x=},{y=}')
                if y > depth:
                    hit_floor = True
                    break
            else:
                j += 1
                j %= len(pattern)
                p = pattern[j]
                if p == '>':
                    x = min(x + 1, tot_width - width)
                    added_shape = grid[y - height:y, x:x + width] + shape
                    if np.any(added_shape > 1):
                        # not moving
                        x = old_x
                    # print(f'pushes right{", nothing happens" if x == tot_width - width else ""}, {x=}, {y=}')
                else:
                    x = max(x - 1, 0)
                    added_shape = grid[y - height:y, x:x + width] + shape
                    if np.any(added_shape > 1):
                        # not moving
                        x = old_x
                    # print(f'pushes left{", nothing happens" if x == 0 else ""}, {x=}, {y=}')
            even = not even
            # wtf, něco se děje, asi bych měl mít y == depth?
            if hit_floor:
                break
            else:
                added_shape = grid[y - height:y, x:x + width] + shape
                if np.any(added_shape > 1):
                    break
        grid[old_y - height:old_y, old_x:old_x + width] += shape
        grid2[old_y - height:old_y, old_x:old_x + width] += shape * i
        blocks[old_y - height:old_height] = i
        heights[i] = max(max_height - (old_y - height), 0)
        old_height = old_y - height
        max_height = min(max_height, old_y - height)
    return grid, blocks, heights, grid2


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()
    shapes = prepare_shapes()
    depth = 6_000
    # depth = 30
    grid, _, _, _ = simulate_tetris(pattern, shapes, depth, 2022)
    return int(depth - np.argmax(np.max(grid, axis=1), axis=0))


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()
    shapes = prepare_shapes()
    depth = 25_000
    sim_steps = 5_000
    target_steps = 1_000_000_000_000
    # target_steps = 2022
    grid, blocks, heights, grid2 = simulate_tetris(pattern, shapes, depth, sim_steps)
    print('computed day 2')

    # each input combination is assigned unique number.
    time_ser = np.sum(grid * np.arange(1, 8), axis=1)[::-1]
    valid_time_ser = time_ser[:np.max(np.where(time_ser > 0)[0])]
    n_lags = min(5_000, len(valid_time_ser) - 1)
    hn_lags = min(5_000, len(heights) - 1)
    acf = sm.tsa.acf(valid_time_ser, nlags=n_lags)  # guess how much to compute
    hacf = sm.tsa.acf(heights, nlags=hn_lags)  # guess how much to compute
    plt.figure(figsize=(10, 8))
    lag = np.arange(n_lags + 1)
    plt.plot(lag, acf)
    plt.xlabel('Lags')
    plt.ylabel('Autocorrelation')
    plt.show()
    plt.figure(figsize=(10, 8))
    lag = np.arange(hn_lags + 1)
    plt.plot(lag, hacf)
    plt.xlabel('Lags')
    plt.ylabel('heights Autocorrelation')
    plt.show()
    period = np.argsort(acf)[::-1][1]
    hperiod = np.argsort(hacf)[::-1][1]
    # for test data, it's 53 period and offset 25
    offset = 0
    for j in range(period):
        a1 = check_period(valid_time_ser[j:], period)
        if np.all(list(map(lambda x: x == 0, a1[:30]))):
            offset = j
            break
    hoffset = 0
    for j in range(hperiod):
        a1 = check_period(heights[j:], hperiod)
        if np.all(list(map(lambda x: x == 0, a1[:30]))):
            hoffset = j
            break
    print(f'found it! {period=}, {offset=}')
    print(f'found it! {hperiod=}, {hoffset=}')

    offset_num = blocks[depth - offset]
    after1period_num = blocks[depth - offset - period]
    period_num = after1period_num - offset_num
    cur_height = np.sum(heights[:hoffset])
    period_height = np.sum(heights[:hoffset + hperiod]) - np.sum(heights[:hoffset])
    cur_blocks = hoffset
    num_periods = (target_steps - offset_num) // hperiod
    cur_height += num_periods * period_height
    cur_blocks += num_periods * hperiod
    # add the part of period
    remaining_blocks = target_steps - cur_blocks
    cur_height += np.sum(heights[hoffset:hoffset+remaining_blocks])
    cur_blocks += remaining_blocks
    return int(cur_height)


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3]
    acf = sm.tsa.acf(arr, nlags=15)
    a1 = check_period(arr, 1)
    a2 = check_period(arr, 2)
    a3 = check_period(arr, 3)
    a4 = check_period(arr, 4)
    a5 = check_period(arr, 5)
    a6 = check_period(arr, 6)
    a7 = check_period(arr, 7)
    a8 = check_period(arr, 8)
    acc = np.correlate(arr, arr, mode='full')
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
