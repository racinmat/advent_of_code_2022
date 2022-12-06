DROP TABLE IF EXISTS dec22;

CREATE UNLOGGED TABLE dec22 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec22 (row_data) FROM '/aoc/days/day_22/input.txt';

