DROP TABLE IF EXISTS dec20;

CREATE TABLE dec20 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec20/input.txt'
VACUUM ANALYZE dec01;
