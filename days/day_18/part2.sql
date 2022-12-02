DROP TABLE IF EXISTS dec18;

CREATE UNLOGGED TABLE dec18 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec18 (value) FROM '/aoc/days/day_18/input.txt';
VACUUM ANALYZE dec18;
