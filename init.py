import os
import os.path as osp
for i in range(1, 26):
    os.makedirs(f'day_{i:02d}', exist_ok=True)
    input_name = f'day_{i:02d}/input.txt'
    if not osp.isfile(input_name):
        open(input_name, 'w+').close()
    with open(f'day_{i:02d}/main.sql', 'w+') as f:
        f.write(f"""\
DROP TABLE IF EXISTS dec{i:02d};

CREATE TABLE dec{i:02d} (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec{i:02d}/input.txt'
VACUUM ANALYZE dec01;
""")
    with open(f'day_{i:02d}/main.py', 'w+') as f:
        f.write(f"""\
import time
from os.path import dirname
import psycopg2
from misc import read_day, submit_day


def execute_day(part: int):
    conn = psycopg2.connect(f"dbname=postgres user=postgres password=example")

    with conn as cursor:
        with open(dirname(__file__) + f"/part{{part}}.sql", "r", encoding="utf-8") as f:
            return cursor.execute(f.read())


if __name__ == '__main__':
    read_day({i})
    tic = time.perf_counter()
    res1 = execute_day(1)
    tac = time.perf_counter()
    res2 = execute_day(2)
    toc = time.perf_counter()
    submit_day(res1, {i}, 1)
    submit_day(res2, {i}, 2)
    print(f"day {i:02d} part 1 in {{tac - tic:0.4f}} seconds")
    print(f"day {i:02d} part 2 in {{toc - tac:0.4f}} seconds")
""")
