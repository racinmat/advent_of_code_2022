DROP TABLE IF EXISTS dec04;

CREATE UNLOGGED TABLE dec04 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data text NOT NULL
);

COPY dec04 (row_data) FROM '/aoc/days/day_04/input.txt';
-- COPY dec04 (row_data) FROM '/aoc/days/day_04/test_input.txt';

WITH ranges as (SELECT line_number,
                       row_data,
                       split_part(split_part(row_data, ',', 1), '-', 1)::int as e1_from,
                       split_part(split_part(row_data, ',', 1), '-', 2)::int as e1_to,
                       split_part(split_part(row_data, ',', 2), '-', 1)::int as e2_from,
                       split_part(split_part(row_data, ',', 2), '-', 2)::int as e2_to
                from dec04
                order by line_number),
     intersections as (select row_data,
                              e1_from,
                              e1_to,
                              e2_from,
                              e2_to,
                              e1_to < e2_from,
                              e2_to < e1_from,
                              1 - (e1_to < e2_from or e2_to < e1_from)::int as intersects
                       from ranges)
select sum(intersects) from intersections;
-- select * from intersections;
