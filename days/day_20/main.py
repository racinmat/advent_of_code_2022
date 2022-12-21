import copy
import time
from os.path import dirname
from pathlib import Path
import numpy as np
from misc import read_day, submit_day, prettytime


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        numbers = [int(i) for i in f.read().split('\n')]
    orig_numbers = copy.copy(numbers)
    orig_indices = list(range(len(orig_numbers)))
    cur_indices = copy.copy(orig_indices)
    print(f'{", ".join(map(str, numbers))}')
    for i in orig_indices:
        val = orig_numbers[i]
        # cur_idx = cur_indices[i]
        # I need inverse search, not direct
        cur_idx = next(filter(lambda xy: xy[1] == i, enumerate(cur_indices)))[0]
        del numbers[cur_idx]
        numbers.insert(cur_idx + val, val)
        del cur_indices[cur_idx]
        cur_indices.insert(cur_idx + val, i)
        print(f'{", ".join(map(str, numbers))}')

def execute_part2():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        numbers = [int(i) for i in f.read().split('\n')]


if __name__ == '__main__':
    read_day(20)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 20, 1)
    # submit_day(res2, 20, 2)
    print(f"day 20 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 20 part 2 in {prettytime(toc - tac)}, answer: {res2}")
