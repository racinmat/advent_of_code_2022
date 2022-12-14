import time
from os.path import dirname
from pathlib import Path
from misc import read_day, submit_day, prettytime
import numpy as np


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    a = [[list(map(int,i.split(','))) for i in l.split(' -> ')] for l in data]
    y_max = max(j[1] for i in a for j in i) + 1
    grid = np.chararray((1000, y_max), itemsize=1)


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n\n')


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
