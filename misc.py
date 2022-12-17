import math
from os.path import dirname
from pathlib import Path

import yaml
from aocd import get_data, submit

with open(dirname(__file__) + '/secret.yaml', 'r') as f:
    token = yaml.safe_load(f)['session']


def read_day(i: int):
    input_path = Path(dirname(__file__)) / 'days' / f'day_{i:02d}' / 'input.txt'
    with open(input_path, 'r', encoding='utf-8') as f:
        in_data = f.read()
    if in_data == '':
        in_data = get_data(token, day=i, year=2022)
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(in_data)
    return in_data


def submit_day(answer, i: int, part: int):
    parts = {1: 'a', 2: 'b'}
    return submit(answer, part=parts[part], day=i, year=2022, session=token)


def prettytime(t):
    t *= 1e9
    if t < 1e3:
        value, units = t, "ns"
    elif t < 1e6:
        value, units = t / 1e3, "μs"
    elif t < 1e9:
        value, units = t / 1e6, "ms"
    else:
        value, units = t / 1e9, "s"

    return f"{value:.3f} {units}"


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
