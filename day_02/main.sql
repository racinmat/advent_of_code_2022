DROP TABLE IF EXISTS dec02;

CREATE TABLE dec02 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec02/input.txt'
VACUUM ANALYZE dec01;
