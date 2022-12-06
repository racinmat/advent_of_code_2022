DROP TABLE IF EXISTS dec10;

CREATE UNLOGGED TABLE dec10 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec10 (row_data) FROM '/aoc/days/day_10/input.txt';

