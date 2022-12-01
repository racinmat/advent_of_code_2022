DROP TABLE IF EXISTS dec16;

CREATE TABLE dec16 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec16 (value) FROM '/aoc/days/day_16/input.txt';
VACUUM ANALYZE dec16;
