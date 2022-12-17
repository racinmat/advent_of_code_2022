import time
from os.path import dirname
from pathlib import Path
from misc import read_day, submit_day, prettytime
import numpy as np
import networkx as nx


def letter2height(x: str) -> int:
    match x:
        case 'S':
            return 0
        case 'E':
            return ord('z') - ord('a')
        case _:
            return ord(x) - ord('a')


def build_graph(data):
    grid = np.array([list(d) for d in data])
    g = nx.grid_2d_graph(*grid.shape, create_using=nx.DiGraph)
    heights = {index: letter2height(x) for index, x in np.ndenumerate(grid)}
    nx.set_node_attributes(g, heights, 'height')
    heights = nx.get_node_attributes(g, 'height')
    sx, sy = np.where(grid == 'S')
    ex, ey = np.where(grid == 'E')
    e2remove = [(n_from, n_to) for n in g.nodes for n_from, n_to in g.edges(n)
                if heights[n_to] - heights[n_from] > 1]
    for e in e2remove:
        g.remove_edge(*e)
    return grid, g, sx, sy, ex, ey


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    grid, g, sx, sy, ex, ey = build_graph(data)
    return nx.shortest_path_length(g, (sx[0], sy[0]), (ex[0], ey[0]))


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    grid, g, sx, sy, ex, ey = build_graph(data)
    a_s = set(zip(*np.where(grid == 'a')))
    paths = nx.single_target_shortest_path_length(g, (ex[0], ey[0]))
    return min(l for (start, l) in paths if start in a_s)


if __name__ == '__main__':
    read_day(12)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 12, 1)
    submit_day(res2, 12, 2)
    print(f"day 12 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 12 part 2 in {prettytime(toc - tac)}, answer: {res2}")
