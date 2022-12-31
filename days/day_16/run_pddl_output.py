import re
from os.path import dirname
from pathlib import Path


def run_it():
    pddl_output = """\
0.0: (move AA II)
1.0: (move II JJ)
2.0: (open_valve JJ)
3.0: (move JJ II)
4.0: (move II AA)
5.0: (move AA BB)
6.0: (open_valve BB)
7.0: (move BB CC)
8.0: (open_valve CC)
9.0: (move CC DD)
10.0: (open_valve DD)
11.0: (move DD EE)
12.0: (open_valve EE)
13.0: (move EE FF)
14.0: (move FF GG)
15.0: (move GG HH)
16.0: (open_valve HH)
17.0: (move HH GG)
18.0: (move GG HH)
19.0: (move HH GG)
20.0: (move GG FF)
21.0: (open_valve FF)
22.0: (move FF GG)
23.0: (move GG FF)
24.0: (move FF GG)
25.0: (open_valve GG)
26.0: (move GG FF)
27.0: (move FF EE)
28.0: (move EE FF)
29.0: (move FF GG)\
"""
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    p = re.compile(
        r'Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<neighbors>(\w+(, )?)*)')
    valves = {}
    for line in data:
        m = p.match(line)
        valve = {'name': m['name'], 'rate': int(m['rate']), 'neighbors': m['neighbors'].split(', ')}
        valves[valve['name']] = valve
    p2 = re.compile(
        r'(?P<minute>\d+)\.0: \((\w+) (\w+)( (\w+))?\)')
    total_rate = 0
    open_valves = []
    total_points = 0
    minimized_cost = 1
    max_points_per_action = (30 * max(v['rate'] for v in valves.values())) + 1

    for line in pddl_output.split("\n"):
        m = p2.match(line)
        minute = int(m['minute']) + 1
        print(f"== Minute {minute} ==")
        if len(open_valves) == 0:
            print(f"No valves are open.")
        elif len(open_valves) == 1:
            print(f"Valve {open_valves[0]} is open, releasing {total_rate} pressure.")
        else:
            valves_str = ", ".join(open_valves[:-1]) + " and " + open_valves[-1]
            print(f"Valves {valves_str} are open, releasing {total_rate} pressure.")
        if m[2] == 'move':
            print(f"You move to valve {m[4][1:]}.")
            minimized_cost += max_points_per_action
        elif m[2] == 'open_valve':
            print(f"You open valve {m[3]}.")
            open_valves.append(m[3])
            total_rate += valves[m[3]]['rate']
            minimized_cost += max_points_per_action - (31 - minute) * valves[m[3]]['rate']
        print(f"{minimized_cost=}")
        total_points += total_rate
    print(f"{total_points=}")
    print(f"{minimized_cost=}")


# Metric (Search):17595.0
if __name__ == '__main__':
    run_it()
