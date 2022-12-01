DROP TABLE IF EXISTS dec24;

CREATE TABLE dec24 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '2022/dec24/input.txt'
VACUUM ANALYZE dec01;
