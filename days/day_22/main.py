import time
from functools import reduce
from os.path import dirname
from pathlib import Path
import numpy as np
from misc import read_day, submit_day, prettytime, Point

EMPTY = 1
WALL = 2
VOID = 3


def add_or_new(arr, char):
    if len(arr) == 0:
        arr.append(char)
    elif isinstance(arr[-1], str) and arr[-1].isnumeric() and char.isnumeric():
        arr[-1] += char
    elif isinstance(arr[-1], str) and arr[-1].isnumeric() and char in ('R', 'L'):
        arr[-1] = int(arr[-1])
        arr.append(char)
    elif isinstance(arr[-1], str) and arr[-1] in ('R', 'L'):
        arr.append(char)
    else:
        print(f'err: {arr=}, {char=}')
    return arr


def find_first(row, comp):
    return int(np.argmax(row == comp))


def find_type(orientation, direction, grid, x, y, val):
    match orientation:
        case 'R':
            return find_first(grid[x, y:y + direction], val)
        case 'L':
            raise NotImplementedError()
        case 'D':
            return find_first(grid[x:x + direction, y], val)
        case 'U':
            raise NotImplementedError()


def all_empty(orientation, direction, grid, x, y):
    match orientation:
        case 'R':
            return np.all(grid[x, y:y + direction] == EMPTY)
        case 'L':
            raise NotImplementedError()
        case 'D':
            return np.all(grid[x:x + direction, y] == EMPTY)
        case 'U':
            raise NotImplementedError()


def go2wall(orientation, wall, x, y):
    match orientation:
        case 'R':
            return Point(x, y + wall - 1)
        case 'L':
            raise NotImplementedError()
        case 'D':
            return Point(x + wall - 1, y)
        case 'U':
            raise NotImplementedError()


def move(grid, pos, orientation, direction):
    if direction == 0:
        return pos
    x, y = pos
    wall = find_type(orientation, direction, grid, x, y, WALL)
    if wall > 0:
        return go2wall(orientation, wall, x, y)
    elif all_empty(orientation, direction, grid, x, y):
        return Point(x, y + direction)
    else:
        void = find_type(orientation, direction, grid, x, y, VOID)
        remaining = direction - void
        if remaining == 0:
            return pos
        else:
            new_y = find_first(grid[x, :], EMPTY)
            move()

def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        maze, directions_str = f.read().split('\n\n')
    rows = maze.split('\n')
    grid = np.zeros((len(rows), max(map(len, rows))), dtype=np.int8)
    for row, grid_line in zip(rows, grid):
        np_row = np.array(list(row))
        grid_line[len(row):] += VOID
        grid_line[:len(row)] += (np_row == ' ') * VOID
        grid_line[:len(row)] += (np_row == '#') * WALL
        grid_line[:len(row)] += (np_row == '.') * EMPTY
    directions = reduce(add_or_new, directions_str, [])
    pos = Point(0, int(np.argmax(grid[0, :] == EMPTY)))
    orientations = ['U', 'R', 'D', 'L']
    orient = 1
    for direction in directions:
        match direction:
            case int():
                x, y = pos
                match orientations[orient]:
                    case 'R':
                        wall = find_first(grid[x, y:y + direction], WALL)
                        if wall > 0:
                            pos = Point(x, y + wall - 1)
                        elif np.all(grid[x, y:y + direction] == EMPTY):
                            pos = Point(x, y + direction)
                        else:
                            void = find_first(grid[x, y:y + direction], VOID)
                            remaining = direction - void
                            if remaining > 0:
                                ...
                            appear_y = find_first(grid[x, :], EMPTY)
                            wall = find_first(grid[x, appear_y:appear_y + remaining], WALL)
                            if wall > 0:
                                pos = Point(x, y + wall - 1)
                            elif np.all(grid[x, appear_y:appear_y + remaining] == EMPTY):
                                pos = Point(x, appear_y + remaining)
                            else:
                                ...
                    case 'U':
                        ...
                    case 'D':
                        wall = find_first(grid[x:x + direction, y], WALL)
                        if wall > 0:
                            pos = Point(x + wall - 1, y)
                        elif np.all(grid[x:x + direction, y] == EMPTY):
                            pos = Point(x + direction, y)
                        else:
                            void = find_first(grid[x: x + direction, y], VOID)
                            remaining = direction - void
                            appear_x = np.argmax(grid[:, x] == EMPTY)
                            wall = find_first(grid[appear_x:appear_x + remaining, y], WALL)
                            if wall > 0:
                                pos = Point(x, y + wall - 1)
                            elif np.all(grid[appear_x:appear_x + remaining, y] == EMPTY):
                                pos = Point(appear_x + remaining, y)
                            else:
                                ...
                    case 'L':
                        ...
            case 'L':
                orient = (orient - 1) % 4
            case 'R':
                orient = (orient + 1) % 4


def execute_part2():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        monkeys_input = f.read().split('\n\n')


if __name__ == '__main__':
    read_day(22)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 22, 1)
    # submit_day(res2, 22, 2)
    print(f"day 22 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 22 part 2 in {prettytime(toc - tac)}, answer: {res2}")
