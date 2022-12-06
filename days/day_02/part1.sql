DROP TABLE IF EXISTS dec02;

CREATE UNLOGGED TABLE dec02 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    orig_text   text   NOT NULL
);

COPY dec02 (orig_text) FROM '/aoc/days/day_02/input.txt';
-- COPY dec02 (orig_text) FROM '/aoc/days/day_02/test_input.txt';

DROP TABLE IF EXISTS d02_rps;

CREATE UNLOGGED TABLE d02_rps
(
    p1        text NOT NULL,
    p2        text NOT NULL,
    points_p2 int  NOT NULL
);

INSERT INTO d02_rps
-- a,x = rock
-- b,y = paper
-- c,z = scissors
values ('A', 'X', 1 + 3), ('A', 'Y', 2 + 6), ('A', 'Z', 3 + 0),
       ('B', 'X', 1 + 0), ('B', 'Y', 2 + 3), ('B', 'Z', 3 + 6),
       ('C', 'X', 1 + 6), ('C', 'Y', 2 + 0), ('C', 'Z', 3 + 3);

with games as (SELECT plays.p1,
                      plays.p2,
                      points_p2
               from (SELECT split_part(orig_text, ' ', 1) as p1,
                            split_part(orig_text, ' ', 2) as p2,
                            line_number
                     from dec02) as plays
                        join d02_rps on plays.p1 = d02_rps.p1 and plays.p2 = d02_rps.p2 order by line_number)
select sum(points_p2)
from games;
