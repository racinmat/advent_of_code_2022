import time
from functools import cmp_to_key
from os.path import dirname
from pathlib import Path
from typing import Optional

from numba import njit

from misc import read_day, submit_day, prettytime

InputType = int | list[int] | list[list[int]] | list[list[list[int]]]


# same signature as cmp so I can use the cmp_to_key
# can't easily speed it up using numba, because it does not support the structural pattern matching
def compare(inp1: InputType, inp2: InputType) -> int:
    match inp1, inp2:
        case int(), int():
            return inp1 - inp2
        case list(), int():
            return compare(inp1, [inp2])
        case int(), list():
            return compare([inp1], inp2)
        case list(), list():
            for i1, i2 in zip(inp1, inp2):
                if (r := compare(i1, i2)) != 0:
                    return r
            return len(inp1) - len(inp2)


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n\n')
    inputs = [list(map(eval, d.split('\n'))) for d in data]
    return sum(k + 1 for k, (i1, i2) in enumerate(map(eval, d.split('\n')) for d in data) if compare(i1, i2))


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    inputs = [eval(d) for d in data if d != ''] + [[[2]], [[6]]]
    inputs.sort(key=cmp_to_key(compare))
    return (inputs.index([[2]]) + 1) * (inputs.index([[6]]) + 1)


if __name__ == '__main__':
    read_day(13)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 13, 1)
    # submit_day(res2, 13, 2)
    print(f"day 13 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 13 part 2 in {prettytime(toc - tac)}, answer: {res2}")
