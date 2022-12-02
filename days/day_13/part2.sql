DROP TABLE IF EXISTS dec13;

CREATE UNLOGGED TABLE dec13 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec13 (value) FROM '/aoc/days/day_13/input.txt';
VACUUM ANALYZE dec13;
