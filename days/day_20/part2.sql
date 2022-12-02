DROP TABLE IF EXISTS dec20;

CREATE UNLOGGED TABLE dec20 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec20 (value) FROM '/aoc/days/day_20/input.txt';
VACUUM ANALYZE dec20;
