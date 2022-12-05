import re
import time
from os.path import dirname
from pathlib import Path
import psycopg2
from misc import read_day, submit_day, prettytime


def parse_crates(crates_data: str) -> dict[int, list[str]]:
    crates_raw = [i[1::4] for i in crates_data.split('\n')]
    ri = reversed(crates_raw)
    col_n = list(map(int, next(ri)))
    crates_d = {k: [] for k in col_n}
    for r in ri:
        for k, c in zip(col_n, r):
            if c != ' ':
                crates_d[k].append(c)
    return crates_d


def parse_moves(moves_line: str) -> tuple[int, int, int]:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', moves_line)
    return int(m[1]), int(m[2]), int(m[3])


def execute_part1():
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
    # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read()
    crates_data, moves_data = data.split('\n\n')
    crates = parse_crates(crates_data)
    moves = map(parse_moves, moves_data.split('\n'))
    for n_crates, c_from, c_to in moves:
        for i in range(n_crates):
            crates[c_to].append(crates[c_from].pop())
    return ''.join(c[-1] for c in crates.values())


def execute_part2():
    with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
    # with open(Path(dirname(__file__)) / f"test_input.txt", "r", encoding="utf-8") as f:
        data = f.read()
    crates_data, moves_data = data.split('\n\n')
    crates = parse_crates(crates_data)
    moves = map(parse_moves, moves_data.split('\n'))
    for n_crates, c_from, c_to in moves:
        crates[c_to] += crates[c_from][-n_crates:]
        del crates[c_from][-n_crates:]
    return ''.join(c[-1] for c in crates.values())


if __name__ == '__main__':
    read_day(5)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 5, 1)
    # submit_day(res2, 5, 2)
    print(f"day 05 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 05 part 2 in {prettytime(toc - tac)}, answer: {res2}")
