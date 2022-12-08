import time
from os.path import dirname
from pathlib import Path
import psycopg2
import numpy as np
from misc import read_day, submit_day, prettytime


def execute_part1():
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
        # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    grid = np.array([list(map(int, d)) for d in data])
    from_top = np.maximum.accumulate(grid, axis=0)
    from_left = np.maximum.accumulate(grid, axis=1)
    from_down = np.flip(np.maximum.accumulate(np.flip(grid, axis=0), axis=0), axis=0)
    from_right = np.flip(np.maximum.accumulate(np.flip(grid, axis=1), axis=1), axis=1)
    from_top_shift = np.pad(from_top, (1, 0), constant_values=-1)[:-1, 1:]
    from_left_shift = np.pad(from_left, (1, 0), constant_values=-1)[1:, :-1]
    from_down_shift = np.pad(from_down, (0, 1), constant_values=-1)[1:, :-1]
    from_right_shift = np.pad(from_right, (0, 1), constant_values=-1)[:-1, 1:]
    visibles = ((grid - from_top_shift) > 0) + ((grid - from_left_shift) > 0) + ((grid - from_down_shift) > 0) + (
            (grid - from_right_shift) > 0)
    return np.sum(visibles)


def execute_part2():
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
        # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read().split('\n')


if __name__ == '__main__':
    read_day(8)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    submit_day(res1, 8, 1)
    # submit_day(res2, 8, 2)
    print(f"day 08 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 08 part 2 in {prettytime(toc - tac)}, answer: {res2}")
