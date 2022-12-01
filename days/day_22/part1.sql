DROP TABLE IF EXISTS dec22;

CREATE TABLE dec22 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec22 (value) FROM '/aoc/days/day_22/input.txt';
VACUUM ANALYZE dec22;
