import time
from os.path import dirname
from pathlib import Path
import psycopg2
from sympy import Symbol, Eq, solveset
from sympy.solvers.solveset import solveset_real

from misc import read_day, submit_day, prettytime


class Monkey(object):
    def __init__(self, name: str, val_or_op):
        self.name = name
        if isinstance(val_or_op, int) or isinstance(val_or_op, Symbol):
            self.val = val_or_op
        else:
            self.val = None
            self.op = val_or_op

    def value(self):
        if self.val is None:
            self.val = self.op()
        print(f'monkey {self.name=} has {self.val=}')
        return self.val


def func_maker(val1, op, val2, monkeys):
    match op:
        case '+':
            return lambda: monkeys[val1].value() + monkeys[val2].value()
        case '-':
            return lambda: monkeys[val1].value() - monkeys[val2].value()
        case '*':
            return lambda: monkeys[val1].value() * monkeys[val2].value()
        case '/':
            return lambda: monkeys[val1].value() / monkeys[val2].value()
        case '=':
            return lambda: Eq(monkeys[val1].value(), monkeys[val2].value())
        case _:
            return lambda: 0  # not needed, but makes static analyser happy


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        monkeys_input = f.read().split('\n')
    monkeys = {}
    for monkey_input in monkeys_input:
        match monkey_input.split(' '):
            case [name_str, val]:
                name = name_str[:-1]
                val = int(val)
                monkeys[name] = Monkey(name, val)
            case [name_str, mon1, op, mon2]:
                name = name_str[:-1]
                monkeys[name] = Monkey(name, func_maker(mon1, op, mon2, monkeys))
    return int(monkeys['root'].value())


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        monkeys_input = f.read().split('\n')
    monkeys = {}
    unknown = Symbol('x')
    for monkey_input in monkeys_input:
        match monkey_input.split(' '):
            case ['humn:', val]:
                name = 'humn'
                monkeys[name] = Monkey(name, unknown)
            case [name_str, val]:
                name = name_str[:-1]
                val = int(val)
                monkeys[name] = Monkey(name, val)
            case ['root:', mon1, op, mon2]:
                name = 'root'
                monkeys[name] = Monkey(name, func_maker(mon1, '=', mon2, monkeys))
            case [name_str, mon1, op, mon2]:
                name = name_str[:-1]
                monkeys[name] = Monkey(name, func_maker(mon1, op, mon2, monkeys))
    expr = monkeys['root'].value()
    return int(next(iter(solveset_real(expr, unknown))))


if __name__ == '__main__':
    read_day(21)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 21, 1)
    # submit_day(res2, 21, 2)
    print(f"day 21 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 21 part 2 in {prettytime(toc - tac)}, answer: {res2}")
