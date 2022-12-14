import time
from os.path import dirname
from pathlib import Path
import psycopg2
from misc import read_day, submit_day, prettytime


def execute_part1():
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")
    with conn:
        with conn.cursor() as cursor:
            with open(Path(dirname(__file__)) / f"part1.sql", "r", encoding="utf-8") as f:
                cursor.execute(f.read())
                return cursor.fetchone()[0]


def execute_part2():
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")
    with conn:
        with conn.cursor() as cursor:
            with open(Path(dirname(__file__)) / f"part2.sql", "r", encoding="utf-8") as f:
                cursor.execute(f.read())
                return cursor.fetchone()[0]


if __name__ == '__main__':
    read_day(25)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    submit_day(res1, 25, 1)
    submit_day(res2, 25, 2)
    print(f"day 25 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 25 part 2 in {prettytime(toc - tac)}, answer: {res2}")
