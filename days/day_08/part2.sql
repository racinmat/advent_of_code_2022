DROP TABLE IF EXISTS dec08;

CREATE UNLOGGED TABLE dec08 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec08 (value) FROM '/aoc/days/day_08/input.txt';
VACUUM ANALYZE dec08;
