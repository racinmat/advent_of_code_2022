import time
from functools import reduce
from os.path import dirname
from pathlib import Path
from typing import Optional

from treelib import Tree, Node
from misc import read_day, submit_day, prettytime


def split2commands(arr: list[list[str]], val: str):
    if val.startswith('$'):
        arr.append([val])
    else:
        arr[-1].append(val)
    return arr


def build_tree(commands: list[list[str]]) -> Tree:
    tree = Tree()
    cur_node: Optional[str] = None
    for comm in commands:
        i = iter(comm)
        command = next(i)
        match command:
            case '$ cd /':
                tree.create_node('/', data={'type': 'dir'})
                cur_node = tree.root
            case '$ ls':
                for obj in i:
                    res1, res2 = obj.split(' ')
                    tree.create_node(res2, parent=cur_node,
                                     data={'type': 'dir'} if res1 == 'dir' else {'type': 'file', 'size': int(res1)})
            case '$ cd ..':
                cur_node = tree.parent(cur_node).identifier
            case com if com.startswith('$ cd '):
                target_dir = com.replace('$ cd ', '')
                cur_node = next(filter(lambda x: x.tag == target_dir, tree.children(cur_node))).identifier
    return tree


def total_size(tree: Tree, root=None) -> int:
    if root is None:
        root = tree.root
    tot_size = tree[root].data.get('size')
    if tot_size is None:
        tot_size = sum(total_size(tree, ch.identifier) for ch in tree.children(root))
        tree[root].data['size'] = tot_size
    return tot_size


def execute_part1():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    commands = reduce(split2commands, data, [])
    tree = build_tree(commands)
    total_size(tree)
    nodes = tree.filter_nodes(lambda x: x.data['size'] <= 100000 and x.data['type'] == 'dir')
    return sum(n.data['size'] for n in nodes)


def execute_part2():
    input_file = "input.txt"
    # input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        data = f.read().split('\n')
    commands = reduce(split2commands, data, [])
    tree = build_tree(commands)
    tot_size = total_size(tree)
    max_size = 70000000
    needed_free_size = 30000000
    free_size = max_size - tot_size
    size2free = needed_free_size - free_size
    nodes = tree.filter_nodes(lambda x: x.data['size'] >= size2free and x.data['type'] == 'dir')
    return min(n.data['size'] for n in nodes)


if __name__ == '__main__':
    read_day(7)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 7, 1)
    # submit_day(res2, 7, 2)
    print(f"day 07 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 07 part 2 in {prettytime(toc - tac)}, answer: {res2}")
# day 07 part 1 in 27.100 ms, answer: 1611443
# day 07 part 2 in 13.876 ms, answer: 2086088
