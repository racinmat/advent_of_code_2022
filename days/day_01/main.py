import time
from functools import reduce
from heapq import nlargest
from os.path import dirname
from pathlib import Path
import psycopg2
from misc import read_day, submit_day, prettytime
import numpy as np


def add_or_new(arr, val):
    if val == 0:
        arr.append(0)
    else:
        arr[-1] += val
    return arr


def execute_part1():
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")

    with conn.cursor() as cursor:
        with open(Path(dirname(__file__)) / f"part1.sql", "r", encoding="utf-8") as f:
            cursor.execute(f.read())
            return cursor.fetchone()[0]
    # with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
    #     # data = [0 if i == '\n' else int(i.strip()) for i in f.readlines()]
    #     data = (0 if i == '\n' else int(i.strip()) for i in f.readlines())
    # return max(reduce(add_or_new, data, [0]))
    # return max(map(sum, np.split(np.array(data), np.where(np.array(data) == 0)[0][1:])))


def execute_part2():
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")

    with conn.cursor() as cursor:
        with open(Path(dirname(__file__)) / f"part2.sql", "r", encoding="utf-8") as f:
            cursor.execute(f.read())
            return cursor.fetchone()[0]
    # with open(Path(dirname(__file__)) / f"input.txt", "r", encoding="utf-8") as f:
    #     # data = [0 if i == '\n' else int(i.strip()) for i in f.readlines()]
    #     data = (0 if i == '\n' else int(i.strip()) for i in f.readlines())
    # return sum(nlargest(3, reduce(add_or_new, data, [0])))


if __name__ == '__main__':
    read_day(1)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    submit_day(res1, 1, 1)
    submit_day(res2, 1, 2)
    print(f"day 01 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 01 part 2 in {prettytime(toc - tac)}, answer: {res2}")
