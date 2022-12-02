DROP TABLE IF EXISTS dec23;

CREATE UNLOGGED TABLE dec23 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec23 (value) FROM '/aoc/days/day_23/input.txt';
VACUUM ANALYZE dec23;
