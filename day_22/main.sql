DROP TABLE IF EXISTS dec22;

CREATE TABLE dec22 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec22/input.txt'
VACUUM ANALYZE dec01;
