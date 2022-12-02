DROP TABLE IF EXISTS dec01;

CREATE UNLOGGED TABLE dec01 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    calories    text
);

COPY dec01 (calories) FROM '/aoc/days/day_01/input.txt';
-- VACUUM ANALYZE dec01;

select max(a_sum)
from (select sum(value) as a_sum
      from (select line_number,
                   value,
                   SUM(CASE WHEN value is null THEN 1 ELSE 0 END) OVER (ORDER BY line_number) AS id
            from (select line_number,
                         nullif(calories, '')::int as value
                  from dec01) as dec01a) as lni
      group by id) as part_sum;
