DROP TABLE IF EXISTS dec18;

CREATE TABLE dec18 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec18/input.txt'
VACUUM ANALYZE dec01;
