DROP TABLE IF EXISTS dec13;

CREATE UNLOGGED TABLE dec13 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec13 (row_data) FROM '/aoc/days/day_13/input.txt';
VACUUM ANALYZE dec13;
