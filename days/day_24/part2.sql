DROP TABLE IF EXISTS dec24;

CREATE UNLOGGED TABLE dec24 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec24 (row_data) FROM '/aoc/days/day_24/input.txt';

