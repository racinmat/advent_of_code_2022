import copy
import time
from os.path import dirname
from pathlib import Path
import my_module

from misc import read_day, submit_day, prettytime


def get_result(numbers, tot_len):
    zero_idx = my_module.find(numbers, 0)
    one_i = (zero_idx + 1_000) % tot_len
    two_i = (zero_idx + 2_000) % tot_len
    three_i = (zero_idx + 3_000) % tot_len
    one = numbers[one_i]
    two = numbers[two_i]
    three = numbers[three_i]
    return one + two + three


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        numbers = [int(i) for i in f.read().split('\n')]
    orig_numbers = copy.copy(numbers)
    orig_indices = list(range(len(orig_numbers)))
    cur_indices = copy.copy(orig_indices)
    tot_len, numbers, _ = my_module.mix_numbers(numbers, orig_numbers, orig_indices, cur_indices)
    return get_result(numbers, tot_len)


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        numbers = [int(i) * 811589153 for i in f.read().split('\n')]
    orig_numbers = copy.copy(numbers)
    orig_indices = list(range(len(orig_numbers)))
    cur_indices = copy.copy(orig_indices)
    tot_len = None
    for i in range(10):
        tot_len, numbers, cur_indices = my_module.mix_numbers(numbers, orig_numbers, orig_indices, cur_indices)
    return get_result(numbers, tot_len)


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
