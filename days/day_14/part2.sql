DROP TABLE IF EXISTS dec14;

CREATE UNLOGGED TABLE dec14 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec14 (row_data) FROM '/aoc/days/day_14/input.txt';

