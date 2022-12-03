DROP TABLE IF EXISTS dec11;

CREATE UNLOGGED TABLE dec11 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec11 (row_data) FROM '/aoc/days/day_11/input.txt';
VACUUM ANALYZE dec11;
