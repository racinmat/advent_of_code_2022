DROP TABLE IF EXISTS dec08;

CREATE TABLE dec08 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec08/input.txt'
VACUUM ANALYZE dec01;
