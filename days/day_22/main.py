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
            return find_first(grid[x, y:y + direction+1], val)
        case 'L':
            return find_first(grid[x, y:max(y - direction-1, 0):-1], val)
        case 'D':
            return find_first(grid[x:x + direction+1, y], val)
        case 'U':
            return find_first(grid[x:max(x - direction-1, 0):-1, y], val)


def all_empty(orientation, direction, grid, x, y):
    match orientation:
        case 'R':
            return np.all(grid[x, y:y + direction] == EMPTY)
        case 'L':
            return np.all(grid[x, y:y - direction:-1] == EMPTY)
        case 'D':
            return np.all(grid[x:x + direction, y] == EMPTY)
        case 'U':
            return np.all(grid[x:x - direction:-1, y] == EMPTY)


def after_wrap(orientation, grid, x, y):
    match orientation:
        case 'R':
            return Point(x, find_first(grid[x, :], EMPTY))
        case 'L':
            return Point(x, grid.shape[1] - find_first(grid[x, ::-1], EMPTY) - 1)
        case 'D':
            return Point(find_first(grid[:, y], EMPTY), y)
        case 'U':
            return Point(grid.shape[0] - find_first(grid[::-1, y], EMPTY) - 1, y)


def goes_outside_grid(orientation, direction, grid, x, y):
    # if all empty, I just go there, if not, I wrap, so going outside of the grid must start wrapping logic
    match orientation:
        case 'R':
            return y + direction >= grid.shape[1]
        case 'L':
            return y - direction < 0
        case 'D':
            return x + direction >= grid.shape[0]
        case 'U':
            return x - direction < 0


def dist2grid_end(orientation, grid, x, y):
    # if all empty, I just go there, if not, I wrap, so going outside of the grid must start wrapping logic
    match orientation:
        case 'R':
            return grid.shape[1] - y
        case 'L':
            return y
        case 'D':
            return grid.shape[0] - x
        case 'U':
            return x


def is_wall_after_wrap(orientation, grid, x, y):
    match orientation:
        case 'R':
            return find_first(grid[x, :], WALL) < find_first(grid[x, :], EMPTY)
        case 'L':
            return find_first(grid[x, ::-1], WALL) < find_first(grid[x, ::-1], EMPTY)
        case 'D':
            return find_first(grid[:, y], WALL) < find_first(grid[:, y], EMPTY)
        case 'U':
            return find_first(grid[::-1, y], WALL) < find_first(grid[::-1, y], EMPTY)


def move_by(orientation, x, y, steps):
    match orientation:
        case 'R':
            return Point(x, y + steps)
        case 'L':
            return Point(x, y - steps)
        case 'D':
            return Point(x + steps, y)
        case 'U':
            return Point(x - steps, y)


def move(grid, pos, orientation, direction):
    if direction == 0:
        return pos
    x, y = pos
    wall = find_type(orientation, direction, grid, x, y, WALL)
    if wall > 0:
        return move_by(orientation, x, y, wall - 1)
    elif all_empty(orientation, direction, grid, x, y) and not goes_outside_grid(orientation, direction, grid, x, y):
        return move_by(orientation, x, y, direction)
    else:
        void_coord = find_type(orientation, direction, grid, x, y, VOID)
        # check that we really go outside and there is not explicit void before us
        if goes_outside_grid(orientation, direction, grid, x, y) and void_coord == 0:
            void = dist2grid_end(orientation, grid, x, y)
        else:
            void = void_coord
        remaining = direction - void
        if remaining == 0 or is_wall_after_wrap(orientation, grid, x, y):
            return move_by(orientation, x, y, void - 1)
        else:
            pos = after_wrap(orientation, grid, x, y)
            return move(grid, pos, orientation, remaining)


def parse_directions(directions_str):
    directions = reduce(add_or_new, directions_str, [])
    if isinstance(directions[-1], str) and directions[-1].isnumeric():
        directions[-1] = int(directions[-1])
    return directions


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
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
    directions = parse_directions(directions_str)
    pos = Point(0, int(np.argmax(grid[0, :] == EMPTY)))
    orientations = ['R', 'D', 'L', 'U']
    orient = 0
    for i, direction in enumerate(directions):
        match direction:
            case int():
                pos = move(grid, pos, orientations[orient], direction)
            case 'L':
                orient = (orient - 1) % 4
            case 'R':
                orient = (orient + 1) % 4
    x, y = pos
    return (x + 1) * 1_000 + (y + 1) * 4 + orient


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
# wrong answer: 116284
# That's not the right answer; your answer is too low.  If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit.  Please wait one minute before trying again. (You guessed 116284.) [Return to Day 22]
