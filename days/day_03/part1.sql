DROP TABLE IF EXISTS dec03;

CREATE UNLOGGED TABLE dec03 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec03 (value) FROM '/aoc/days/day_03/input.txt';
VACUUM ANALYZE dec03;
