DROP TABLE IF EXISTS dec20;

CREATE UNLOGGED TABLE dec20 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec20 (row_data) FROM '/aoc/days/day_20/input.txt';

