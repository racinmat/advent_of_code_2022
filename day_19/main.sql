DROP TABLE IF EXISTS dec19;

CREATE TABLE dec19 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec19/input.txt'
VACUUM ANALYZE dec01;
