DROP TABLE IF EXISTS dec19;

CREATE TABLE dec19 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec19 (value) FROM '/aoc/days/day_19/input.txt';
VACUUM ANALYZE dec19;
