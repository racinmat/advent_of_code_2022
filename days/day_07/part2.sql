DROP TABLE IF EXISTS dec07;

CREATE UNLOGGED TABLE dec07 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec07 (row_data) FROM '/aoc/days/day_07/input.txt';

