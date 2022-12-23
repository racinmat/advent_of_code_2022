import re
import time
from os.path import dirname
from pathlib import Path

from unified_planning import model
from unified_planning.engines import PlanGenerationResultStatus
from unified_planning.io import PDDLWriter
from unified_planning.model import Fluent, InstantaneousAction, Object, Problem
from unified_planning.shortcuts import UserType, BoolType, Not, IntType, Equals, GT, Times, OneshotPlanner

from misc import read_day, prettytime


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    p = re.compile(
        r'Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<neighbors>(\w+(, )?)*)')
    valves = []
    for line in data:
        m = p.match(line)
        valve = {'name': m['name'], 'rate': int(m['rate']), 'neighbors': m['neighbors'].split(', ')}
        valves.append(valve)

    # Declaring types
    location = UserType("Location")

    # Creating problem ‘variables’
    position = Fluent("position", BoolType(), location=location)
    remaining_time = Fluent("remaining_time", IntType(0, 30))
    total_points = Fluent("total_points", IntType(0))
    is_connected = Fluent(
        "is_connected", BoolType(), location_1=location, location_2=location
    )
    # formulating as valve closed so I don't have negative preconditions
    valve_closed = Fluent(
        "valve_closed", BoolType(), location=location
    )
    flow_rate = Fluent("flow_rate", IntType(0), location=location)

    # Creating actions
    move = InstantaneousAction("move", l_from=location, l_to=location)
    open_valve = InstantaneousAction("open_valve", at=location)
    l_from = move.parameter("l_from")
    l_to = move.parameter("l_to")
    at = open_valve.parameter("at")

    move.add_precondition(GT(remaining_time, 0))
    move.add_precondition(position(l_from))
    # negative preconditions are hard, should not be needed, if position is removed correctly
    # move.add_precondition(Not(position(l_to)))
    # I have predicates for both directions
    move.add_precondition(is_connected(l_from, l_to))
    move.add_effect(position(l_from), False)
    move.add_effect(position(l_to), True)
    move.add_decrease_effect(remaining_time, 1)

    open_valve.add_precondition(GT(remaining_time, 0))
    open_valve.add_precondition(position(at))
    open_valve.add_precondition(valve_closed(at))
    open_valve.add_decrease_effect(remaining_time, 1)
    open_valve.add_increase_effect(total_points, Times(flow_rate(at), remaining_time))
    open_valve.add_effect(valve_closed(at), False)

    # Populating the problem with initial state and goals
    problem = Problem("valves_problem")

    problem.add_fluent(position)
    problem.add_fluent(remaining_time)
    problem.add_fluent(total_points)
    problem.add_fluent(is_connected)
    problem.add_fluent(valve_closed)
    problem.add_fluent(flow_rate)

    problem.add_action(move)
    problem.add_action(open_valve)

    # Declaring objects
    valve_names = [v['name'] for v in valves]
    valve_vars = {}
    for valve in valves:
        v = Object(valve['name'], location)
        valve_vars[valve['name']] = v
        problem.add_object(v)
        if valve['name'] == 'AA':
            problem.set_initial_value(position(v), True)
        else:
            problem.set_initial_value(position(v), False)
        problem.set_initial_value(valve_closed(v), True)
        problem.set_initial_value(flow_rate(v), valve['rate'])

    for valve in valves:
        for other in valve_names:
            if other in valve['neighbors']:
                problem.set_initial_value(is_connected(valve_vars[valve['name']], valve_vars[other]), True)
            else:
                problem.set_initial_value(is_connected(valve_vars[valve['name']], valve_vars[other]), False)

    problem.set_initial_value(total_points, 0)
    problem.set_initial_value(remaining_time, 30)
    problem.add_goal(Equals(remaining_time, 0))
    problem.add_quality_metric(model.metrics.MaximizeExpressionOnFinalState(total_points()))

    w = PDDLWriter(problem)
    w.write_domain('valves_domain.pddl')
    w.write_problem('valves_problem.pddl')
    with open('valves_domain.pddl', 'r', encoding='utf-8') as f:
        domain_str = f.read()
    with open('valves_problem.pddl', 'r', encoding='utf-8') as f:
        problem_str = f.read()
    with open('valves_domain.pddl', 'w', encoding='utf-8') as f:
        f.write(domain_str.replace('\r\n', '\n')
                .replace(' :numeric-fluents)', ' :fluents)')
                )
    with open('valves_problem.pddl', 'w', encoding='utf-8') as f:
        f.write(problem_str.replace('\r\n', '\n')
                .replace('integer[0, inf] total_points', '(total_points)')
                )

    # with OneshotPlanner(problem_kind=problem.kind, optimality_guarantee=PlanGenerationResultStatus.SOLVED_OPTIMALLY) as planner:
    #     # Asking the planner to solve the problem
    #     plan = planner.solve(problem)
    #
    #     # Printing the plan
    #     print(plan)


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
# todo: search https://github.com/nergmada/planning-wiki/search?p=2&q=numeric which good numeric planners are there
# try some of suggested here https://stackoverflow.com/a/71421101/5224881

# todo: instead of maximizing score, minimize it.
# if we would have cost (max score+1) for all actions, both opening valves and moving, and valve opening would have
# price the high cost - the points we obtain, and we still stop after 30 actions, it should work
# usually this maximization -> minimization leads to preference of lower amount of edges/shorter path, but now we need
# strictly 30 actions/edges.
