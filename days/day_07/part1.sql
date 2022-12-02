DROP TABLE IF EXISTS dec07;

CREATE UNLOGGED TABLE dec07 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec07 (value) FROM '/aoc/days/day_07/input.txt';
VACUUM ANALYZE dec07;
