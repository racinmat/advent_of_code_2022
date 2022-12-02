DROP TABLE IF EXISTS dec02;

CREATE UNLOGGED TABLE dec02 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value text NOT NULL
);

COPY dec02 (value) FROM '/aoc/days/day_02/input.txt';
-- VACUUM ANALYZE dec02;
