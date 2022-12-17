import math
import time
from os.path import dirname
from pathlib import Path
from misc import read_day, submit_day, prettytime, Point

directions = {
    'R': Point(0, 1),
    'L': Point(0, -1),
    'U': Point(1, 0),
    'D': Point(-1, 0),
}


def run_part1(moves: list):
    head_pos = Point(0, 0)
    tail_pos = Point(0, 0)
    positions = {tail_pos}
    for direction, length in moves:
        vec = directions[direction]
        for i in range(length):
            prev_head_pos = head_pos
            head_pos += vec
            if head_pos.dist(tail_pos) > 1:
                tail_pos = prev_head_pos
                positions.add(tail_pos)
    return positions


def execute_part1():
    # I tried numba, but set of jit classes does not work and putting it to list is still very slow
    input_file = "input.txt"
    # input_file = ftest_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    moves = [(n[0], int(n[1])) for d in data if (n := d.split(' '))]
    # print(len(positions))
    positions = run_part1(moves)
    # return len(set(positions))
    return len(positions)


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    moves = [(n[0], int(n[1])) for d in data if (n := d.split(' '))]
    # grid = np.zeros((5, 6), dtype=int)
    head_pos = Point(0, 0)
    tail_positions = [Point(0, 0) for i in range(9)]
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
                    if moved_diagonally:  # if head has moved diagonally, the rules are different
                        prev_head_pos = tail_pos + ((a_head_pos - tail_pos) / 2).round_away_from_zero()
                    tail_pos = prev_head_pos
                    tail_positions[j] = tail_pos
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
