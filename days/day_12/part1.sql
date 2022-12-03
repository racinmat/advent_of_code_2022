DROP TABLE IF EXISTS dec12;

CREATE UNLOGGED TABLE dec12 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec12 (row_data) FROM '/aoc/days/day_12/input.txt';
VACUUM ANALYZE dec12;
