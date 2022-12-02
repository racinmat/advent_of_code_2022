DROP TABLE IF EXISTS dec17;

CREATE UNLOGGED TABLE dec17 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec17 (value) FROM '/aoc/days/day_17/input.txt';
VACUUM ANALYZE dec17;
