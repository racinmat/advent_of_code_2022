DROP TABLE IF EXISTS dec17;

CREATE UNLOGGED TABLE dec17 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec17 (row_data) FROM '/aoc/days/day_17/input.txt';

