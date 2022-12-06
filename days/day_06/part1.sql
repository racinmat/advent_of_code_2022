DROP TABLE IF EXISTS dec06;

CREATE UNLOGGED TABLE dec06 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec06 (row_data) FROM '/aoc/days/day_06/input.txt';
