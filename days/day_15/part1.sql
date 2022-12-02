DROP TABLE IF EXISTS dec15;

CREATE UNLOGGED TABLE dec15 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec15 (value) FROM '/aoc/days/day_15/input.txt';
VACUUM ANALYZE dec15;
