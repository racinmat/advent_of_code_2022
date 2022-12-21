# Advent of Code 2022 in Python or SQL

Solutions of annual coding challenge https://adventofcode.com/ written in PostgreSQL and Python 
(python as a fallback if SQL would be too annoying).

Benchmarks


## Initialization

Run this to create conda env:
```bash
conda create -n aoc2022 -c conda-forge python=3.10 poetry
conda activate aoc2022
poetry init
poetry add advent-of-code-data psycopg2 PyYAML treelib numpy
```

Run `python init.py` to generate base parts of the code base for each day.

In order to download the input data programatically, log in to adventofcode.com, and then grab the cookie token and put it to `secret.yaml`.

Run the db by `docker-compose up -d`

solvers for day 16 downloaded from
https://sites.google.com/view/enhsp/?pli=1
https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html
https://cw.fel.cvut.cz/old/_media/courses/a4m36pah/assignments/planners64.zip

the compiled.py must be ran before the main.py, if present, to compile the numba code.