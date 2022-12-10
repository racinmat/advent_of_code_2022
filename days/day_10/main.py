import re
import time
from os.path import dirname
from pathlib import Path
import numpy as np
from misc import read_day, submit_day, prettytime


def add_strength(cycle, register, tot_strength):
    if (cycle - 20) % 40 == 0:
        return tot_strength + cycle * register
    return tot_strength


def execute_instructions(instructions, register, perform_tick):
    for instruction in instructions:
        match instruction.split(' '):
            case ['noop']:
                register = perform_tick(register)
            case ['addx', x] if re.match(r'-?\d+', x):
                register = perform_tick(register)
                register = perform_tick(register)
                register += int(x)
    return register


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    cycle, register, tot_strength = 0, 1, 0

    def perform_tick(register):
        nonlocal cycle, tot_strength
        cycle += 1
        tot_strength = add_strength(cycle, register, tot_strength)
        return register

    execute_instructions(data, register, perform_tick)
    return tot_strength


def draw2grid(cycle, register, grid):
    grid[np.unravel_index(cycle, grid.shape)] = '#' if register - 1 <= (cycle % 40) <= register + 1 else '.'


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    cycle, register, grid = 0, 1, np.chararray((6, 40), itemsize=1)
    grid[:] = ' '

    def perform_tick(register):
        nonlocal cycle, grid
        draw2grid(cycle, register, grid)
        cycle += 1
        return register

    execute_instructions(data, register, perform_tick)
    grid[grid == b'.'] = ' '
    np.apply_along_axis(lambda x: print(x.tostring()), axis=1, arr=grid)
    return 'PLGFKAZG'


if __name__ == '__main__':
    read_day(10)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 10, 1)
    # submit_day(res2, 10, 2)
    print(f"day 10 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 10 part 2 in {prettytime(toc - tac)}, answer: {res2}")
