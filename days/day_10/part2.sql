DROP TABLE IF EXISTS dec10;

CREATE UNLOGGED TABLE dec10 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec10 (value) FROM '/aoc/days/day_10/input.txt';
VACUUM ANALYZE dec10;
