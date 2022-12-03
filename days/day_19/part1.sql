DROP TABLE IF EXISTS dec19;

CREATE UNLOGGED TABLE dec19 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec19 (row_data) FROM '/aoc/days/day_19/input.txt';
VACUUM ANALYZE dec19;
