DROP TABLE IF EXISTS dec18;

CREATE UNLOGGED TABLE dec18 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec18 (row_data) FROM '/aoc/days/day_18/input.txt';

