import copy
import time
from os.path import dirname
from pathlib import Path
import numpy as np
from misc import read_day, submit_day, prettytime


def find(cur_indices, i):
    return next(filter(lambda xy: xy[1] == i, enumerate(cur_indices)))[0]


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        numbers = [int(i) for i in f.read().split('\n')]
    orig_numbers = copy.copy(numbers)
    tot_len = len(orig_numbers)
    orig_indices = list(range(len(orig_numbers)))
    cur_indices = copy.copy(orig_indices)
    print(f'{", ".join(map(str, numbers))}')
    for i in orig_indices:
        assert len(set(cur_indices)) == len(cur_indices) == tot_len
        val = orig_numbers[i]
        # I need inverse search, not direct
        cur_idx = find(cur_indices, i)
        new_idx = (cur_idx + val)
        if new_idx >= tot_len:
            new_idx = (new_idx % tot_len) + (new_idx // tot_len)
        elif new_idx < -tot_len:
            new_idx = -(-new_idx % tot_len) - (-new_idx // tot_len)
        del numbers[cur_idx]
        numbers.insert(new_idx, val)
        del cur_indices[cur_idx]
        cur_indices.insert(new_idx, i)
        # print(f'{", ".join(map(str, numbers))}')
    zero_idx = find(numbers, 0)
    one_i = (zero_idx + 1_000) % tot_len
    two_i = (zero_idx + 2_000) % tot_len
    three_i = (zero_idx + 3_000) % tot_len
    one = numbers[one_i]
    two = numbers[two_i]
    three = numbers[three_i]
    return one + two + three


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
