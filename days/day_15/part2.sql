DROP TABLE IF EXISTS dec15;

CREATE UNLOGGED TABLE dec15 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec15 (row_data) FROM '/aoc/days/day_15/input.txt';

