import time
from os.path import dirname
import psycopg2
from misc import read_day, submit_day


def execute_day(part: int):
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")

    with conn as cursor:
        with open(dirname(__file__) + f"/part{part}.sql", "r", encoding="utf-8") as f:
            return cursor.execute(f.read())


if __name__ == '__main__':
    read_day(14)
    tic = time.perf_counter()
    res1 = execute_day(1)
    tac = time.perf_counter()
    res2 = execute_day(2)
    toc = time.perf_counter()
    submit_day(res1, 14, 1)
    submit_day(res2, 14, 2)
    print(f"day 14 part 1 in {tac - tic:0.4f} seconds")
    print(f"day 14 part 2 in {toc - tac:0.4f} seconds")
