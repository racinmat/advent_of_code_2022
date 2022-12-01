DROP TABLE IF EXISTS dec13;

CREATE TABLE dec13 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec13/input.txt'
VACUUM ANALYZE dec01;
