DROP TABLE IF EXISTS dec12;

CREATE TABLE dec12 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec12 (value) FROM '/aoc/days/day_12/input.txt';
VACUUM ANALYZE dec12;
