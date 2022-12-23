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
            return find_first(grid[x, y:y + direction + 1], val)
        case 'L':
            return find_first(grid[x, y::-1], val) if (y - direction - 1 < 0) else find_first(
                grid[x, y:y - direction - 1:-1], val)
        case 'D':
            return find_first(grid[x:x + direction + 1, y], val)
        case 'U':
            return find_first(grid[x::-1, y], val) if (x - direction - 1 < 0) else find_first(
                grid[x:x - direction - 1:-1, y], val)


def all_empty(orientation, direction, grid, x, y):
    match orientation:
        case 'R':
            return np.all(grid[x, y:y + direction + 1] == EMPTY)
        case 'L':
            return np.all(grid[x, y::-1] == EMPTY) if (y - direction - 1 < 0) else np.all(
                grid[x, y:y - direction - 1:-1] == EMPTY)
        case 'D':
            return np.all(grid[x:x + direction + 1, y] == EMPTY)
        case 'U':
            return np.all(grid[x::-1, y] == EMPTY) if (x - direction - 1 < 0) else np.all(
                grid[x:x - direction - 1:-1, y] == EMPTY)


def after_wrap_plane(orientation, grid, x, y):
    match orientation:
        case 'R':
            return Point(x, find_first(grid[x, :], EMPTY))
        case 'L':
            return Point(x, grid.shape[1] - find_first(grid[x, ::-1], EMPTY) - 1)
        case 'D':
            return Point(find_first(grid[:, y], EMPTY), y)
        case 'U':
            return Point(grid.shape[0] - find_first(grid[::-1, y], EMPTY) - 1, y)


def after_wrap_cube(orientations, orient, grid, x, y, wrappings, steps):
    orientation = orientations[orient]
    x_edge, y_edge = move_by(orientation, x, y, steps)
    x_edge2, y_edge2, orient_change = wrappings[x_edge, y_edge, orient]
    return Point(x_edge2, y_edge2), (orient + orient_change) % 4


def goes_outside_grid(orientation, direction, grid, x, y):
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
    match orientation:
        case 'R':
            return grid.shape[1] - y
        case 'L':
            return y + 1
        case 'D':
            return grid.shape[0] - x
        case 'U':
            return x + 1


def is_wall_after_wrap(orientations, orient, grid, x, y, is_cube, wrappings, steps):
    orientation = orientations[orient]
    if is_cube:
        pos, _ = after_wrap_cube(orientations, orient, grid, x, y, wrappings, steps)
        return grid[tuple(pos)] == WALL
    else:
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


def move(grid, pos, orientations, orient, direction, is_cube, wrappings):
    assert not is_cube or len(wrappings) > 10
    orientation = orientations[orient]
    if direction == 0:
        return orient, pos
    x, y = pos
    wall = find_type(orientation, direction, grid, x, y, WALL)
    if wall > 0:
        return orient, move_by(orientation, x, y, wall - 1)
    elif all_empty(orientation, direction, grid, x, y) and not goes_outside_grid(orientation, direction, grid, x, y):
        return orient, move_by(orientation, x, y, direction)
    else:
        void_coord = find_type(orientation, direction, grid, x, y, VOID)
        # check that we really go outside and there is no explicit void before us
        if goes_outside_grid(orientation, direction, grid, x, y) and void_coord == 0:
            void = dist2grid_end(orientation, grid, x, y)
        else:
            void = void_coord
        remaining = direction - void
        if is_wall_after_wrap(orientations, orient, grid, x, y, is_cube, wrappings, void - 1):
            return orient, move_by(orientation, x, y, void - 1)
        else:
            if is_cube:
                pos, orient = after_wrap_cube(orientations, orient, grid, x, y, wrappings, void - 1)
            else:
                pos = after_wrap_plane(orientation, grid, x, y)
            return move(grid, pos, orientations, orient, remaining, is_cube, wrappings)


def parse_directions(directions_str):
    directions = reduce(add_or_new, directions_str, [])
    if isinstance(directions[-1], str) and directions[-1].isnumeric():
        directions[-1] = int(directions[-1])
    return directions


def parse_grid(maze):
    rows = maze.split('\n')
    grid = np.zeros((len(rows), max(map(len, rows))), dtype=np.int8)
    for row, grid_line in zip(rows, grid):
        np_row = np.array(list(row))
        grid_line[len(row):] += VOID
        grid_line[:len(row)] += (np_row == ' ') * VOID
        grid_line[:len(row)] += (np_row == '#') * WALL
        grid_line[:len(row)] += (np_row == '.') * EMPTY
    return grid


def run_maze(directions, grid, is_cube, wrappings=None):
    pos = Point(0, int(np.argmax(grid[0, :] == EMPTY)))
    orientations = ['R', 'D', 'L', 'U']
    orient = 0
    for i, direction in enumerate(directions):
        match direction:
            case int():
                orient, pos = move(grid, pos, orientations, orient, direction, is_cube, wrappings)
            case 'L':
                orient = (orient - 1) % 4
            case 'R':
                orient = (orient + 1) % 4
        # print(f'end of direction={direction}, position={pos.x},{pos.y}')
    return orient, pos


def compute_wrappings(grid):
    # just hard-coding it for test case and my case
    smaller_side, larger_side = min(grid.shape), max(grid.shape)
    assert larger_side * 3 == smaller_side * 4
    side = smaller_side // 3
    mappings = {}
    if grid[grid.shape[0] - 1, 0] != VOID and grid[0, grid.shape[1] - 1] != VOID:
        # my shape
        # 1
        y1 = side * 2 - 1
        x2 = side - 1
        for x1, y2 in zip(range(side, side * 2), range(side * 2, side * 3)):
            mappings[x1, y1, 0] = (x2, y2, +3)
            mappings[x2, y2, 1] = (x1, y1, -3)
        # 2
        y1 = side * 2 - 1
        y2 = side * 3 - 1
        for x1, x2 in zip(range(side * 2, side * 3), range(side - 1, -1, -1)):
            mappings[x1, y1, 0] = (x2, y2, +2)
            mappings[x2, y2, 0] = (x1, y1, -2)
        # 3
        x1 = side * 4 - 1
        x2 = 0
        for y1, y2 in zip(range(0, side), range(side * 2, side * 3)):
            mappings[x1, y1, 1] = (x2, y2, +0)
            mappings[x2, y2, 3] = (x1, y1, -0)
        # 4
        y1 = 0
        x2 = 0
        for x1, y2 in zip(range(side * 3, side * 4), range(side, side*2)):
            mappings[x1, y1, 2] = (x2, y2, +3)
            mappings[x2, y2, 3] = (x1, y1, -3)
        # 5
        y1 = 0
        y2 = side
        for x1, x2 in zip(range(side * 2, side * 3), range(side - 1, - 1, -1)):
            mappings[x1, y1, 2] = (x2, y2, +2)
            mappings[x2, y2, 2] = (x1, y1, -2)
        # 6
        x1 = side * 2
        y2 = side
        for y1, x2 in zip(range(0, side), range(side, side * 2)):
            mappings[x1, y1, 3] = (x2, y2, +1)
            mappings[x2, y2, 2] = (x1, y1, -1)
        # 7
        y1 = side - 1
        x2 = side * 3 - 1
        for x1, y2 in zip(range(side * 3, side * 4), range(side, side * 2)):
            mappings[x1, y1, 0] = (x2, y2, +3)
            mappings[x2, y2, 1] = (x1, y1, -3)
    elif grid[grid.shape[0] - 1, grid.shape[1] - 1] != VOID and grid[0, grid.shape[1] - 1] == VOID:
        # test shape
        # 1
        x1 = side
        x2 = 0
        for y1, y2 in zip(range(0, side), range(side * 3 - 1, side * 2 - 1, -1)):
            mappings[x1, y1, 3] = (x2, y2, +2)
            mappings[x2, y2, 3] = (x1, y1, -2)
        # 2
        x1 = side
        y2 = side * 2
        for y1, x2 in zip(range(side, side * 2), range(0, side)):
            mappings[x1, y1, 3] = (x2, y2, +1)
            mappings[x2, y2, 2] = (x1, y1, -1)
        # 3
        y1 = side * 3 - 1
        y2 = side * 4 - 1
        for x1, x2 in zip(range(0, side), range(side * 3 - 1, side * 2 - 1, -1)):
            mappings[x1, y1, 0] = (x2, y2, +2)
            mappings[x2, y2, 0] = (x1, y1, -2)
        # 4
        y1 = side * 3 - 1
        x2 = side * 2
        for x1, y2 in zip(range(side, side * 2), range(side * 4 - 1, side * 3 - 1, -1)):
            mappings[x1, y1, 0] = (x2, y2, +1)
            mappings[x2, y2, 3] = (x1, y1, -1)
        # 5
        y1 = 0
        x2 = side * 3 - 1
        for x1, y2 in zip(range(side, side * 2), range(side * 4, side * 3 - 1, -1)):
            mappings[x1, y1, 2] = (x2, y2, +1)
            mappings[x2, y2, 1] = (x1, y1, -1)
        # 6
        x1 = side * 2 - 1
        x2 = side * 3 - 1
        for y1, y2 in zip(range(0, side), range(side * 3 - 1, side * 2 - 1, -1)):
            mappings[x1, y1, 1] = (x2, y2, +2)
            mappings[x2, y2, 1] = (x1, y1, -2)
        # 7
        x1 = side * 2 - 1
        y2 = side * 2
        for y1, x2 in zip(range(side, side * 2), range(side * 3 - 1, side * 2 - 1, -1)):
            mappings[x1, y1, 1] = (x2, y2, +3)
            mappings[x2, y2, 2] = (x1, y1, -3)
    else:
        raise NotImplementedError()
    return mappings


def compute_password(orient, pos):
    x, y = pos
    return (x + 1) * 1_000 + (y + 1) * 4 + orient


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        maze, directions_str = f.read().split('\n\n')
    grid = parse_grid(maze)
    directions = parse_directions(directions_str)
    orient, pos = run_maze(directions, grid, False)
    return compute_password(orient, pos)


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        maze, directions_str = f.read().split('\n\n')
    grid = parse_grid(maze)
    wrappings = compute_wrappings(grid)
    directions = parse_directions(directions_str)
    orient, pos = run_maze(directions, grid, True, wrappings)
    return compute_password(orient, pos)


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
# wrong answer: 143020
# That's not the right answer; your answer is too high.  If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit.  Please wait one minute before trying again. (You guessed 143020.) [Return to Day 22]
