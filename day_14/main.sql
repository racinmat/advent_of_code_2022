CREATE SCHEMA IF NOT EXISTS aoc2022;
SET SCHEMA 'aoc2022';
DROP TABLE IF EXISTS dec14;

CREATE TABLE dec14 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec14/input.txt'
VACUUM ANALYZE dec01;
