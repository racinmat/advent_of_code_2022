DROP TABLE IF EXISTS dec11;

CREATE UNLOGGED TABLE dec11 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec11 (value) FROM '/aoc/days/day_11/input.txt';
VACUUM ANALYZE dec11;
