DROP TABLE IF EXISTS dec07;

CREATE TABLE dec07 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec07/input.txt'
VACUUM ANALYZE dec01;
