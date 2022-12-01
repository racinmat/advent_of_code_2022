DROP TABLE IF EXISTS dec01;

CREATE TABLE dec01 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec01 (value) FROM '/aoc/days/day_01/input.txt';
VACUUM ANALYZE dec01;
