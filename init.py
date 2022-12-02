import os
import os.path as osp

for i in range(1, 26):
    os.makedirs(f'days/day_{i:02d}', exist_ok=True)
    input_name = f'days/day_{i:02d}/input.txt'
    if not osp.isfile(input_name):
        open(input_name, 'w+').close()
    with open(f'days/day_{i:02d}/__init__.py', 'w+') as f:
        f.write('')
    with open(f'days/day_{i:02d}/part1.sql', 'w+') as f:
        f.write(f"""\
DROP TABLE IF EXISTS dec{i:02d};

CREATE UNLOGGED TABLE dec{i:02d} (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec{i:02d} (value) FROM '/aoc/days/day_{i:02d}/input.txt';
VACUUM ANALYZE dec{i:02d};
""")
    with open(f'days/day_{i:02d}/part2.sql', 'w+') as f:
        f.write(f"""\
DROP TABLE IF EXISTS dec{i:02d};

CREATE UNLOGGED TABLE dec{i:02d} (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec{i:02d} (value) FROM '/aoc/days/day_{i:02d}/input.txt';
VACUUM ANALYZE dec{i:02d};
""")
    with open(f'days/day_{i:02d}/main.py', 'w+') as f:
        f.write(f"""\
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
    read_day({i})
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    submit_day(res1, {i}, 1)
    submit_day(res2, {i}, 2)
    print(f"day {i:02d} part 1 in {{prettytime(tac - tic)}}, answer: {{res1}}")
    print(f"day {i:02d} part 2 in {{prettytime(toc - tac)}}, answer: {{res2}}")
""")
