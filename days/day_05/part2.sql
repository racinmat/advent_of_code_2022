DROP TABLE IF EXISTS dec05;

CREATE UNLOGGED TABLE dec05 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec05 (value) FROM '/aoc/days/day_05/input.txt';
VACUUM ANALYZE dec05;
