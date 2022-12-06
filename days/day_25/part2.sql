DROP TABLE IF EXISTS dec25;

CREATE UNLOGGED TABLE dec25 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec25 (row_data) FROM '/aoc/days/day_25/input.txt';

