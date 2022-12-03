DROP TABLE IF EXISTS dec16;

CREATE UNLOGGED TABLE dec16 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec16 (row_data) FROM '/aoc/days/day_16/input.txt';
VACUUM ANALYZE dec16;
