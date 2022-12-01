DROP TABLE IF EXISTS dec15;

CREATE TABLE dec15 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec15/input.txt'
VACUUM ANALYZE dec01;
