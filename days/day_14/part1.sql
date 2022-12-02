DROP TABLE IF EXISTS dec14;

CREATE UNLOGGED TABLE dec14 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec14 (value) FROM '/aoc/days/day_14/input.txt';
VACUUM ANALYZE dec14;
