DROP TABLE IF EXISTS dec04;

CREATE UNLOGGED TABLE dec04 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec04 (value) FROM '/aoc/days/day_04/input.txt';
VACUUM ANALYZE dec04;
