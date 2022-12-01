DROP TABLE IF EXISTS dec09;

CREATE TABLE dec09 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec09 (value) FROM '/aoc/days/day_09/input.txt';
VACUUM ANALYZE dec09;
