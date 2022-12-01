DROP TABLE IF EXISTS dec09;

CREATE TABLE dec09 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec09/input.txt'
VACUUM ANALYZE dec01;
