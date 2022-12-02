DROP TABLE IF EXISTS dec25;

CREATE UNLOGGED TABLE dec25 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec25 (value) FROM '/aoc/days/day_25/input.txt';
VACUUM ANALYZE dec25;
