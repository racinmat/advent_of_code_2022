DROP TABLE IF EXISTS dec24;

CREATE TABLE dec24 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

COPY dec24 (value) FROM '/aoc/days/day_24/input.txt';
VACUUM ANALYZE dec24;
