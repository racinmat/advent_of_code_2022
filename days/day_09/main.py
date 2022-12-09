import math
import time
from os.path import dirname
from pathlib import Path
import numpy as np

# from numba import int32, njit, typed
# from numba.experimental import jitclass

from misc import read_day, submit_day, prettytime


# spec = [
#     ('x', int32),
#     ('y', int32),
# ]
#
# @jitclass(spec)
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            return Point(self.x - other, self.y - other)

    def dist(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def man_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f'Point({self.x},{self.y})'

    def __floordiv__(self, other):
        return Point(self.x // other, self.y // other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def ceildiv(self, other):
        # https://stackoverflow.com/a/72864305/5224881
        return -(-self // 2)

    def __ceil__(self):
        return Point(math.ceil(self.x), math.ceil(self.y))

    def __floor__(self):
        return Point(math.floor(self.x), math.floor(self.y))

    def round_away_from_zero(self):
        return Point(math.floor(self.x) if self.x < 0 else math.ceil(self.x),
                     math.floor(self.y) if self.y < 0 else math.ceil(self.y))


def run_part1(moves: list):
    directions = {
        'R': Point(0, 1),
        'L': Point(0, -1),
        'U': Point(1, 0),
        'D': Point(-1, 0),
    }
    head_pos = Point(0, 0)
    tail_pos = Point(0, 0)
    # positions = [tail_pos]
    positions = {tail_pos}
    for direction, length in moves:
        vec = directions[direction]
        for i in range(length):
            prev_head_pos = head_pos
            head_pos += vec
            if head_pos.dist(tail_pos) > 1:
                tail_pos = prev_head_pos
                # positions.append(tail_pos)
                positions.add(tail_pos)
    return positions


def execute_part1():
    # I tried numba, but set of jit classes does not work and putting it to list is still very slow
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
        # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    moves = [(n[0], int(n[1])) for d in data if (n := d.split(' '))]
    # print(len(positions))
    positions = run_part1(moves)
    # return len(set(positions))
    return len(positions)


def execute_part2():
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
    # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    moves = [(n[0], int(n[1])) for d in data if (n := d.split(' '))]
    directions = {
        'R': Point(0, 1),
        'L': Point(0, -1),
        'U': Point(1, 0),
        'D': Point(-1, 0),
    }
    # grid = np.zeros((5, 6), dtype=int)
    head_pos = Point(0, 0)
    tail_positions = [Point(0, 0) for i in range(9)]
    positions = {tail_positions[0]}
    t_positions = {tail_positions[0]}
    # grid[tuple(tail_positions[0])] = 10
    for direction, length in moves:
        vec = directions[direction]
        for i in range(length):
            prev_head_pos = head_pos
            head_pos += vec
            a_head_pos = head_pos
            moved_diagonally = False
            for j, t in enumerate(tail_positions):
                tail_pos = t
                prev_tail = tail_pos
                if a_head_pos.dist(tail_pos) > 1:
                    # if head has moved diagonally, the rules are different
                    if moved_diagonally:
                        # prev_head_pos = tail_pos + (a_head_pos - tail_pos).ceildiv(2)
                        # prev_head_pos = tail_pos + math.ceil((a_head_pos - tail_pos) / 2)
                        prev_head_pos = tail_pos + ((a_head_pos - tail_pos) / 2).round_away_from_zero()
                    tail_pos = prev_head_pos
                    tail_positions[j] = tail_pos
                    positions.add(tail_pos)
                    if j == 8:
                        t_positions.add(tail_pos)
                    # grid[tuple(tail_pos)] = j + 1
                    moved_diagonally = tail_pos.man_dist(prev_tail) > 1
                a_head_pos = tail_pos
                prev_head_pos = prev_tail
    return len(t_positions)


if __name__ == '__main__':
    read_day(9)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 9, 1)
    # submit_day(res2, 9, 2)
    print(f"day 09 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 09 part 2 in {prettytime(toc - tac)}, answer: {res2}")
