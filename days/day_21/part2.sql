DROP TABLE IF EXISTS dec21;

CREATE UNLOGGED TABLE dec21 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec21 (row_data) FROM '/aoc/days/day_21/input.txt';
VACUUM ANALYZE dec21;
