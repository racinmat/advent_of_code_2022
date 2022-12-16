import re
import time
from os.path import dirname
from pathlib import Path
import psycopg2
from unified_planning.model import Fluent, InstantaneousAction, Object, Problem
from unified_planning.shortcuts import UserType, BoolType, GE, Not, Minus, RealType

from misc import read_day, submit_day, prettytime


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    p = re.compile(r'Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<neighbors>(\w+(, )?)*)')
    valves = []
    for line in data:
        m = p.match(line)
        valve = {'name': m['name'], 'rate': m['rate'], 'neighbors': m['neighbors'].split(', ')}
        valves.append(valve)

    # Declaring types
    Location = UserType("Location")

    # Creating problem ‘variables’
    robot_at = Fluent("robot_at", BoolType(), location=Location)
    battery_charge = Fluent("battery_charge", RealType(0, 100))

    # Creating actions
    move = InstantaneousAction("move", l_from=Location, l_to=Location)
    l_from = move.parameter("l_from")
    l_to = move.parameter("l_to")
    move.add_precondition(GE(battery_charge, 10))
    move.add_precondition(robot_at(l_from))
    move.add_precondition(Not(robot_at(l_to)))
    move.add_effect(robot_at(l_from), False)
    move.add_effect(robot_at(l_to), True)
    move.add_effect(battery_charge, Minus(battery_charge, 10))

    # Declaring objects
    l1 = Object("l1", Location)
    l2 = Object("l2", Location)

    # Populating the problem with initial state and goals
    problem = Problem("robot")
    problem.add_fluent(robot_at)
    problem.add_fluent(battery_charge)
    problem.add_action(move)
    problem.add_object(l1)
    problem.add_object(l2)
    problem.set_initial_value(robot_at(l1), True)
    problem.set_initial_value(robot_at(l2), False)
    problem.set_initial_value(battery_charge, 100)
    problem.add_goal(robot_at(l2))


def execute_part2():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')


if __name__ == '__main__':
    read_day(16)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 16, 1)
    # submit_day(res2, 16, 2)
    print(f"day 16 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 16 part 2 in {prettytime(toc - tac)}, answer: {res2}")
