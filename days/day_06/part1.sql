DROP TABLE IF EXISTS dec06;

CREATE TABLE dec06 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec06 (value) FROM '/aoc/days/day_06/input.txt';
VACUUM ANALYZE dec06;
