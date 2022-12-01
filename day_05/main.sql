DROP TABLE IF EXISTS dec05;

CREATE TABLE dec05 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec05/input.txt'
VACUUM ANALYZE dec01;
