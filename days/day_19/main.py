import re
import time
from itertools import product
from os.path import dirname
from pathlib import Path
from typing import Iterable
import nographs as nog
from nographs import Traversal

from misc import read_day, submit_day, prettytime


class Blueprint(object):

    def __init__(self, number: int, ore_bot_price: int, clay_bot_price: int, obs_bot_price: tuple[int, int],
                 geode_bot_price: tuple[int, int]) -> None:
        super().__init__()
        self.number = number
        self.ore_bot_price = ore_bot_price
        self.clay_bot_price = clay_bot_price
        self.obs_bot_price = obs_bot_price
        self.geode_bot_price = geode_bot_price

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Blueprint):
            return self.number == o.number
        return False

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return f"Blueprint(number={self.number},ore_bot={self.ore_bot_price},clay_bot={self.clay_bot_price}," \
               f"obs_bot={self.obs_bot_price},geode_bot={self.geode_bot_price})"


def ignore_none(a, b):
    return a if a is not None else b


class PlanState(object):

    def __init__(self, blueprint: Blueprint, time=0, ore=0, clay=0, obs=0, geode=0, ore_bots=1, clay_bots=0, obs_bots=0,
                 geode_bots=0, skip_clay_bot=False, skip_obs_bot=False, skip_geode_bot=False) -> None:
        super().__init__()
        self.blueprint = blueprint
        self.time = time
        self.ore = ore
        self.clay = clay
        self.obs = obs
        self.geode = geode
        self.ore_bots = ore_bots
        self.clay_bots = clay_bots
        self.obs_bots = obs_bots
        self.geode_bots = geode_bots
        self.skip_clay_bot = skip_clay_bot
        self.skip_obs_bot = skip_obs_bot
        self.skip_geode_bot = skip_geode_bot

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PlanState):
            return False
        return self.blueprint == o.blueprint and self.ore == o.ore and self.clay == o.clay and self.obs == o.obs and \
            self.geode == o.geode and self.ore_bots == o.ore_bots and self.clay_bots == o.clay_bots and \
            self.obs_bots == o.obs_bots and self.geode_bots == o.geode_bots and \
            self.skip_clay_bot == o.skip_clay_bot and self.skip_obs_bot == o.skip_obs_bot and \
            self.skip_geode_bot == o.skip_geode_bot

    def __hash__(self) -> int:
        return hash((self.blueprint, self.ore, self.clay, self.obs, self.geode, self.ore_bots, self.clay_bots,
                     self.obs_bots, self.geode_bots, self.skip_clay_bot, self.skip_obs_bot, self.skip_geode_bot))

    def copy_with(self, ore=None, clay=None, obs=None, geode=None, ore_bots=None, clay_bots=None, obs_bots=None,
                  geode_bots=None, skip_clay_bot=None, skip_obs_bot=None, skip_geode_bot=None):
        return PlanState(self.blueprint, self.time, ignore_none(ore, self.ore), ignore_none(clay, self.clay),
                         ignore_none(obs, self.obs), ignore_none(geode, self.geode),
                         ignore_none(ore_bots, self.ore_bots), ignore_none(clay_bots, self.clay_bots),
                         ignore_none(obs_bots, self.obs_bots), ignore_none(geode_bots, self.geode_bots),
                         ignore_none(skip_clay_bot, self.skip_clay_bot), ignore_none(skip_obs_bot, self.skip_obs_bot),
                         ignore_none(skip_geode_bot, self.skip_geode_bot))

    def __repr__(self) -> str:
        return f"PlanState(blueprint={repr(self.blueprint)},time={self.time},ore={self.ore},clay={self.clay}," \
               f"obs={self.obs},geode={self.geode},ore_bots={self.ore_bots},clay_bots={self.clay_bots}," \
               f"obs_bots={self.obs_bots},geode_bots={self.geode_bots},skip_clay_bot={self.skip_clay_bot}," \
               f"skip_obs_bot={self.skip_obs_bot},skip_geode_bot={self.skip_geode_bot})"


def simulate_and_get_children(s: PlanState, t: Traversal) -> Iterable[PlanState]:
    if s.time == 24:
        return
    s = s.copy_with()
    s.time += 1
    # building bot takes 1 minute, so I can simulate that by using only the resources I had on beginning
    ore = s.ore
    clay = s.clay
    obs = s.obs
    geode = s.geode
    s.ore += s.ore_bots
    s.clay += s.clay_bots
    s.obs += s.obs_bots
    s.geode += s.geode_bots
    geode_b_ore, geode_b_obs = s.blueprint.geode_bot_price
    obs_b_ore, obs_b_clay = s.blueprint.obs_bot_price
    clay_b_ore = s.blueprint.clay_bot_price
    ore_b_ore = s.blueprint.ore_bot_price
    if ore >= geode_b_ore and obs >= geode_b_obs and not s.skip_geode_bot:
        # print(f"""
        # == Minute {s.time} ==
        # Spend {geode_b_ore} ore and {geode_b_obs} obsidian to build a geode-collecting bot.
        # {s.ore_bots} ore-collecting robots; you now have {s.ore - geode_b_ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs - geode_b_obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        for skip_obs, skip_clay in product([True, False], [True, False]):
            yield s.copy_with(ore=s.ore - geode_b_ore, obs=s.obs - geode_b_obs, geode_bots=s.geode_bots + 1,
                              skip_obs_bot=skip_obs, skip_clay_bot=skip_clay)
        # print(f"""
        # == Minute {s.time} ==
        # {s.ore_bots} ore-collecting robots; you now have {s.ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        for skip_obs, skip_clay in product([True, False], [True, False]):
            yield s.copy_with(skip_geode_bot=True, skip_obs_bot=skip_obs, skip_clay_bot=skip_clay)
    elif ore >= obs_b_ore and clay >= obs_b_clay and not s.skip_obs_bot:
        # print(f"""
        # == Minute {s.time} ==
        # Spend {obs_b_ore} ore and {obs_b_clay} clay to build an obsidian-collecting bot.
        # {s.ore_bots} ore-collecting robots; you now have {s.ore - obs_b_ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay - obs_b_clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        for skip_clay in [True, False]:
            yield s.copy_with(ore=s.ore - obs_b_ore, clay=s.clay - obs_b_clay, obs_bots=s.obs_bots + 1,
                              skip_geode_bot=False, skip_clay_bot=skip_clay)
        # print(f"""
        # == Minute {s.time} ==
        # {s.ore_bots} ore-collecting robots; you now have {s.ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        for skip_clay in [True, False]:
            yield s.copy_with(skip_obs_bot=True, skip_geode_bot=False, skip_clay_bot=skip_clay)
    elif ore >= clay_b_ore and not s.skip_clay_bot:
        # print(f"""
        # == Minute {s.time} ==
        # Spend {clay_b_ore} to build a clay-collecting bot.
        # {s.ore_bots} ore-collecting robots; you now have {s.ore - clay_b_ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        yield s.copy_with(ore=s.ore - clay_b_ore, clay_bots=s.clay_bots + 1, skip_geode_bot=False, skip_obs_bot=False)
        # print(f"""
        # == Minute {s.time} ==
        # {s.ore_bots} ore-collecting robots; you now have {s.ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        yield s.copy_with(skip_clay_bot=True, skip_obs_bot=False, skip_geode_bot=False)
    elif ore >= ore_b_ore:
        # print(f"""
        # == Minute {s.time} ==
        # Spend {ore_b_ore} ore to build an ore-collecting bot.
        # {s.ore_bots} ore-collecting robots; you now have {s.ore - ore_b_ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        yield s.copy_with(ore=s.ore - ore_b_ore, ore_bots=s.ore_bots + 1, skip_geode_bot=False, skip_obs_bot=False,
                          skip_clay_bot=False)
    else:
        # print(f"""
        # == Minute {s.time} ==
        # {s.ore_bots} ore-collecting robots; you now have {s.ore} ore.
        # {s.clay_bots} clay-collecting robot collects 1 clay; you now have {s.clay} clay.
        # {s.obs_bots} obs-collecting robot collects 1 clay; you now have {s.obs} obsidian.
        # {s.geode_bots} geode-collecting robot collects 1 clay; you now have {s.geode} geodes.
        #     """)
        yield s


def parse_blueprint(moves_line: str) -> Blueprint:
    m = re.match(
        r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.',
        moves_line)
    return Blueprint(int(m[1]), int(m[2]), int(m[3]), (int(m[4]), int(m[5])), (int(m[6]), int(m[7])))


def find_best_plan(blueprint: Blueprint):
    traversal = nog.TraversalDepthFirst(simulate_and_get_children, is_tree=True).start_from(PlanState(blueprint),
                                                                                            build_paths=True)
    goals_f = filter(lambda s: s.time == 24, traversal)
    goals_f = filter(lambda s: s.geode > 7, goals_f)
    goals = list(goals_f)
    paths = [traversal.paths[g] for g in goals]
    my_paths = [p for p in paths if p[11].obs_bots == 1]
    my_paths2 = [p for p in my_paths if not p[11].skip_clay_bot]
    return goals


def execute_part1():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        lines = f.read().split('\n')
    blueprints = [parse_blueprint(line) for line in lines]
    for blueprint in blueprints:
        a_res = find_best_plan(blueprint)
    return blueprints


def execute_part2():
    # input_file = "input.txt"
    input_file = "test_input.txt"
    with open(Path(dirname(__file__)) / input_file, "r", encoding="utf-8") as f:
        coords_str = [i.split(',') for i in f.read().split('\n')]


if __name__ == '__main__':
    read_day(19)
    tic = time.perf_counter()
    res1 = execute_part1()
    tac = time.perf_counter()
    res2 = execute_part2()
    toc = time.perf_counter()
    # submit_day(res1, 19, 1)
    # submit_day(res2, 19, 2)
    print(f"day 19 part 1 in {prettytime(tac - tic)}, answer: {res1}")
    print(f"day 19 part 2 in {prettytime(toc - tac)}, answer: {res2}")
    # it seems there is too much branching even in the dummy case, I need a pruning heuristic, maybe similar trick to day 16?