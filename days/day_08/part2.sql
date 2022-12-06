DROP TABLE IF EXISTS dec08;

CREATE UNLOGGED TABLE dec08 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec08 (row_data) FROM '/aoc/days/day_08/input.txt';

