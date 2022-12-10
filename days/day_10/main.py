import re
import time
from functools import partial
from os.path import dirname
from pathlib import Path
import numpy as np
from misc import read_day, submit_day, prettytime


def add_strength(cycle, register, tot_strength):
    if (cycle - 20) % 40 == 0:
        return tot_strength + cycle * register
    return tot_strength


def tick(cycle: int, fun: callable):
    cycle += 1
    return cycle, fun(cycle)

# def execute_instructions(instructions):

def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    cycle = 0
    register = 1
    tot_strength = 0
    for instruction in data:
        match instruction.split(' '):
            case ['noop']:
                cycle, tot_strength = tick(cycle, partial(add_strength, register=register, tot_strength=tot_strength))
            case ['addx', x] if re.match(r'-?\d+', x):
                cycle, tot_strength = tick(cycle, partial(add_strength, register=register, tot_strength=tot_strength))
                cycle, tot_strength = tick(cycle, partial(add_strength, register=register, tot_strength=tot_strength))
                register += int(x)
        # print(f'{instruction=}, {cycle=}, {register=}, {tot_strength=}')
    return tot_strength


def draw_grid(cycle, register, grid):
    grid[np.unravel_index(cycle, grid.shape)] = '#' if register - 1 <= (cycle % 40) <= register + 1 else '.'


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    cycle = -1
    register = 1
    grid = np.chararray((6, 40), itemsize=1)
    grid[:] = ' '
    for instruction in data:
        match instruction.split(' '):
            case ['noop']:
                cycle, _ = tick(cycle, partial(draw_grid, register=register, grid=grid))
            case ['addx', x] if re.match(r'-?\d+', x):
                cycle, _ = tick(cycle, partial(draw_grid, register=register, grid=grid))
                cycle, _ = tick(cycle, partial(draw_grid, register=register, grid=grid))
                register += int(x)
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
