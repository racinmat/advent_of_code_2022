DROP TABLE IF EXISTS dec06;

CREATE TABLE dec06 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec06/input.txt'
VACUUM ANALYZE dec01;
