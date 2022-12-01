DROP TABLE IF EXISTS dec11;

CREATE TABLE dec11 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec11/input.txt'
VACUUM ANALYZE dec01;
