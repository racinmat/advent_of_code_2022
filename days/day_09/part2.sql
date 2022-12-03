DROP TABLE IF EXISTS dec09;

CREATE UNLOGGED TABLE dec09 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec09 (row_data) FROM '/aoc/days/day_09/input.txt';
VACUUM ANALYZE dec09;
