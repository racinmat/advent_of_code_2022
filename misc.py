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
