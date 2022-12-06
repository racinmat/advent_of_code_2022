DROP TABLE IF EXISTS dec23;

CREATE UNLOGGED TABLE dec23 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec23 (row_data) FROM '/aoc/days/day_23/input.txt';

