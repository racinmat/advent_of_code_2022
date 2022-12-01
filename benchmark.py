import time

import psycopg2

from misc import read_day, submit_day

max_day = 1


def execute_day(d: int, part: int):
    conn = psycopg2.connect(f"dbname=dec{d:02d} user=postgres password=example")

    with conn as cursor:
        with open(f"day{d:02d}/part{part}.sql", "r", encoding="utf-8") as f:
            return cursor.execute(f.read())


for day in range(1, max_day+1):
    read_day(day)
    tic = time.perf_counter()
    res1 = execute_day(day, 1)
    tac = time.perf_counter()
    res2 = execute_day(day, 2)
    toc = time.perf_counter()
    # submit_day(res1, day, 1)
    # submit_day(res2, day, 2)
    print(f"day {day:02d} part 1 in {tac - tic:0.4f} seconds")
    print(f"day {day:02d} part 2 in {toc - tac:0.4f} seconds")


# MAX_Y_VALUE = 1
#
# directories = []
# for filename in os.listdir('.'):
#     if os.path.isdir(os.path.join('.', filename)):
#         directories.append(filename)
#
# files = [os.path.join(x, "benchmark.json") for x in directories]
#
# benchmark_data = {"Python": {}, "Golang": {}, "Nim": {}}  # adding dicts here sets the order of points being plotted
#
# for filename in files:
#     fpath = os.path.join(path, filename)
#     try:
#         f = open(fpath)
#     except FileNotFoundError:
#         print(f"Warning: missing file {fpath}")
#         continue
#
#     data = json.load(f)
#     f.close()
#
#     for language in data["implementations"]:
#         x = benchmark_data.get(language, {})
#         x[str(data["day"]) + ".1"] = data["implementations"][language]["part.1.avg"]
#         x[str(data["day"]) + ".2"] = data["implementations"][language]["part.2.avg"]
#         benchmark_data[language] = x
#
# all_days = set()
#
# for key in benchmark_data[lang]:
#         day = int(key.split(".", 1)[0])
#         all_days.add(day)
#
# figure = plt.figure(figsize=(len(all_days) / 2, 5))
# axp1 = figure.add_subplot(1, 2, 1)
# axp2 = figure.add_subplot(1, 2, 2, sharey=axp1)
#
# for i, language in enumerate(benchmark_data):
#
#     data = benchmark_data[language]
#     part_one_times = []
#     part_two_times = []
#     days = []
#
#     for key in data:
#
#         day = int(key.split(".", 1)[0])
#         if day not in days:
#             days.append(day)
#
#         if key.endswith(".1"):
#             part_one_times.append(data[key])
#         if key.endswith(".2"):
#             part_two_times.append(data[key])
#
#     colour = COLOURS.get(language)
#
#     p1 = axp1.scatter(days, part_one_times, color=colour)
#     p2 = axp2.scatter(days, part_two_times, color=colour)
#
#     for i, day in enumerate(days):
#         if i + 1 >= len(days):
#             continue
#         if days[i + 1] == day + 1:
#             axp1.plot((day, days[i + 1]), (part_one_times[i], part_one_times[i + 1]), "-", color=colour)
#             axp2.plot((day, days[i + 1]), (part_two_times[i], part_two_times[i + 1]), "-", color=colour)
#
# figure.suptitle(f"Average {YEAR} challenge running time")
# axp1.set_title("Part one")
# axp2.set_title("Part two")
#
#
# def do_auxillary_parts(axis):
#     plt.sca(axis)
#     plt.xticks(list(all_days), [str(y) for y in all_days])
#     plt.ylabel("Running time (seconds)")
#     plt.xlabel("Day")
#     plt.legend(handles=[patches.Patch(color=COLOURS[label], label=label) for label in COLOURS])
#     # plt.ylim([0, MAX_Y_VALUE])
#     # plt.legend(legends)
#
#
# do_auxillary_parts(axp1)
# do_auxillary_parts(axp2)
#
# plt.tight_layout()
# plt.savefig(OUTPUT_FILE)