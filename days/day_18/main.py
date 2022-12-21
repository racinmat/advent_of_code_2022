import time
from collections import Counter
from itertools import combinations
from os.path import dirname
from pathlib import Path

import numpy as np
from Geometry3D import Point
from scipy.spatial import distance_matrix

from misc import read_day, submit_day, prettytime


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        coords_str = [i.split(',') for i in f.read().split('\n')]
    points = np.array([[int(i), int(j), int(k)] for i, j, k in coords_str])
    dists = distance_matrix(points, points)

    # groups = []
    # for i in range(len(points)):
    #     added2group = False
    #     for g in groups:
    #         if any(dists[i, j] == 1. for j in g):
    #             g.append(i)
    #             added2group = True
    #             break
    #     if not added2group:
    #         groups.append([i])

    total_area = 0
    for p in range(len(points)):
        d_count = sum(dists[p, p2] == 1. for p2 in range(len(points)))
        total_area += 6 - int(d_count)

    # group_areas = []
    # for g in groups:
    #     group_area = 0
    #     if len(g) == 1:
    #         group_area += 6
    #     else:
    #         for p in g:
    #             d_count = sum(dists[p, p2] == 1. for p2 in g)
    #             group_area += 6 - d_count
    #     group_areas.append(group_area)
    #     total_area += group_area
    return total_area


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        pattern = f.read()


if __name__ == '__main__':
    read_day(18)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 18, 1)
    # submit_day(res2, 18, 2)
    print(f"day 18 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 18 part 2 in {prettytime(toc - tac)}, answer: {res2}")
# 2022-12-21 14:09:01,045 [Geometry3D WARNING] wrong answer: 10500
# That's not the right answer; your answer is too high.  If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit.  Please wait one minute before trying again. (You guessed 10500.) [Return to Day 18]
