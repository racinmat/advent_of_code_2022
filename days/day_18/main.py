import time
from itertools import combinations, product
from os.path import dirname
from pathlib import Path
import numpy as np
from scipy.spatial import distance_matrix

from misc import read_day, submit_day, prettytime


def group_points(dists, points):
    groups = []
    for i in range(len(points)):
        added2group = False
        for g in groups:
            if any(dists[i, j] == 1. for j in g):
                g.append(i)
                added2group = True
                break
        if not added2group:
            groups.append([i])
    mins = compute_mins(dists, groups)
    while np.any(mins == 1.):
        new_groups = []
        processed_groups = set()
        for i, g in enumerate(groups):
            if i in processed_groups:
                continue
            new_g = g
            processed_groups.add(i)
            for j in np.where(mins[i, :] == 1.)[0]:
                if j in processed_groups:
                    continue
                new_g += groups[j]
                processed_groups.add(j)
            new_groups.append(new_g)
        groups = new_groups

        mins = compute_mins(dists, groups)
    return groups


def compute_mins(dists, groups):
    mins = np.zeros((len(groups), len(groups)))
    for i, j in combinations(range(len(groups)), 2):
        a_dist = dists[groups[i]][:, groups[j]].min()
        mins[i, j] = a_dist
        mins[j, i] = a_dist
    return mins


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        coords_str = [i.split(',') for i in f.read().split('\n')]
    points = np.array([[int(i), int(j), int(k)] for i, j, k in coords_str])
    dists = distance_matrix(points, points)
    total_area = 0
    for p in range(len(points)):
        d_count = sum(dists[p, p2] == 1. for p2 in range(len(points)))
        total_area += 6 - int(d_count)
    return total_area


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        coords_str = [i.split(',') for i in f.read().split('\n')]
    points = np.array([[int(i), int(j), int(k)] for i, j, k in coords_str])
    assert (1, 1, 1) not in list(map(tuple, points))
    min_x, min_y, min_z = np.min(points, axis=0)
    max_x, max_y, max_z = np.max(points, axis=0)
    tot_points = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
    num_empty_points = tot_points - len(points)
    points_set = set(tuple(i) for i in points)
    empty_points = np.array(
        [i for i in product(range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)) if
         tuple(i) not in points_set])
    dists = distance_matrix(points, points)
    groups = group_points(dists, points)
    empty_dists = distance_matrix(empty_points, empty_points)
    empty_groups = group_points(empty_dists, empty_points)
    external_group = next(i for i, g in enumerate(empty_groups) if 0 in g)
    del empty_groups[external_group]

    total_area = 0
    group_areas = []
    for g in groups:
        group_area = 0
        if len(g) == 1:
            group_area += 6
        else:
            for p in g:
                d_count = sum(dists[p, p2] == 1. for p2 in g)
                group_area += 6 - d_count
        group_areas.append(group_area)
        total_area += group_area

    total_bubble_area = 0
    group_areas = []
    for g in empty_groups:
        group_area = 0
        if len(g) == 1:
            group_area += 6
        else:
            for p in g:
                d_count = sum(empty_dists[p, p2] == 1. for p2 in g)
                group_area += 6 - d_count
        group_areas.append(group_area)
        total_bubble_area += group_area

    # too low, it seems there are sides I miss and taking max and mix is not enough
    return int(total_area) - int(total_bubble_area)


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
# You guessed 1784
# That's not the right answer; your answer is too low. If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit. Please wait one minute before trying again. (You guessed 1784.) [Return to Day 18]
# You guessed 2212

# That's not the right answer; your answer is too low. If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit. Please wait one minute before trying again. (You guessed 2212.) [Return to Day 18]
