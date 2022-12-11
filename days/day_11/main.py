import copy
import heapq
import math
import re
import time
import types
from functools import reduce
from os.path import dirname
from pathlib import Path
from typing import Callable, Optional

from misc import read_day, submit_day, prettytime


class Monkey(object):
    def __init__(self, n: int, items: list[int], update_f: Callable[[int], int], divisor: int, m_true: int,
                 m_false: int):
        self.n = n
        self.items = items
        self.update_f = update_f
        self.divisor = divisor
        self.m_true = m_true
        self.m_false = m_false
        self.obtained_items = []
        self.inspections = 0

    def do(self, monkeys: list['Monkey'], part: int, lcm: Optional[int] = None):
        # print(f'Monkey: {self.n}:')
        for i in self.items:
            self.inspections += 1
            # print(f'  Worry level: {i}')
            i = self.update_f(i)
            if part == 1:
                i //= 3
            elif lcm is not None:
                i %= lcm
            # print(f'  New worry level: {i}')
            target = self.m_true if i % self.divisor == 0 else self.m_false
            # print(f'  Throwing item to monkey {target}')
            monkeys[target].items.append(i)
        self.items = []


def func_maker(op, operand_str):
    match op, operand_str:
        case ('*', 'old'):
            return lambda x: x ** 2
        case ('+', 'old'):
            return lambda x: x * 2
        case ('*', i):
            return lambda x: x * int(i)
        case ('+', i):
            return lambda x: x + int(i)
        case _:
            return lambda x: x  # not needed, but makes static analyser happy


def parse_monkeys(data: str):
    monkeys_input = data.split('\n\n')
    monkeys = []
    for monkey_input in monkeys_input:
        match [s.split(' ') for s in monkey_input.split('\n')]:
            case [
                ['Monkey', n_str],
                ['', '', 'Starting', 'items:', *start_items],
                [*_, 'Operation:', 'new', '=', 'old', op, operand_str],
                [*_, 'Test:', 'divisible', 'by', divisor_str],
                [*_, 'If', 'true:', 'throw', 'to', 'monkey', m_true_str],
                [*_, 'If', 'false:', 'throw', 'to', 'monkey', m_false_str]
            ]:
                n = int(n_str[:-1])
                items = [int(i) for i in ''.join(start_items).split(',')]
                update_f = func_maker(op, operand_str)
                divisor = int(divisor_str)
                m_true = int(m_true_str)
                m_false = int(m_false_str)

                # print(f'{n=}, {items=}, {op=}, {update_f=}, {divisor=}, {m_true=}, {m_false=}')
                monkeys.append(Monkey(n, items, update_f, divisor, m_true, m_false))
    return monkeys


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read()
    monkeys = parse_monkeys(data)
    for n in range(20):
        for monkey in monkeys:
            monkey.do(monkeys, 1)
        # for monkey in monkeys:
        #     print(f'Monkey: {monkey.n}: {monkey.items}')
    # for monkey in monkeys:
    #     print(f'Monkey: {monkey.n}: {monkey.inspections=}')
    return math.prod(heapq.nlargest(2, map(lambda x: x.inspections, monkeys)))


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read()
    monkeys = parse_monkeys(data)
    lcm = math.lcm(*map(lambda x: x.divisor, monkeys))
    for n in range(10_000):
        for monkey in monkeys:
            monkey.do(monkeys, 2, lcm)
        # print(f'== After round {n + 1} ==')
        # for monkey in monkeys:
        #     print(f'Monkey: {monkey.n}: {monkey.inspections=}')
    # for monkey in monkeys:
    #     print(f'Monkey: {monkey.n}: {monkey.inspections=}')
    return math.prod(heapq.nlargest(2, map(lambda x: x.inspections, monkeys)))


if __name__ == '__main__':
    read_day(11)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 11, 1)
    submit_day(res2, 11, 2)
    print(f"day 11 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 11 part 2 in {prettytime(toc - tac)}, answer: {res2}")
