DROP TABLE IF EXISTS dec21;

CREATE TABLE dec21 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec21 (value) FROM '/aoc/days/day_21/input.txt';
VACUUM ANALYZE dec21;