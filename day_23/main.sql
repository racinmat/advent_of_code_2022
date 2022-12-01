DROP TABLE IF EXISTS dec23;

CREATE TABLE dec23 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec23/input.txt'
VACUUM ANALYZE dec01;
