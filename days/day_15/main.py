import time
from os.path import dirname
from pathlib import Path
from misc import read_day, submit_day, prettytime


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')


if __name__ == '__main__':
    read_day(15)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 15, 1)
    # submit_day(res2, 15, 2)
    print(f"day 15 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 15 part 2 in {prettytime(toc - tac)}, answer: {res2}")
