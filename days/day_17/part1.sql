DROP TABLE IF EXISTS dec17;

CREATE TABLE dec17 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec17 (value) FROM '/aoc/days/day_17/input.txt';
VACUUM ANALYZE dec17;
