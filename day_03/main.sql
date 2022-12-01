DROP TABLE IF EXISTS dec03;

CREATE TABLE dec03 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec03/input.txt'
VACUUM ANALYZE dec01;
