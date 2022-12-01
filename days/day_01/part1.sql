DROP TABLE IF EXISTS dec01;

CREATE TABLE dec01
(
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value       text
);

COPY dec01 (value) FROM '/aoc/days/day_01/input.txt';
VACUUM ANALYZE dec01;

-- select value, lead(value) over () from dec01;
select line_number, value, value = '' as val_isempty
      from dec01;
select line_number, value, value = '' as val_isempty
      from dec01;

select line_number, value, val_isempty,
       dense_rank() over (
           partition by val_isempty
           order by line_number
           )
from (select line_number, value, value = '' as val_isempty
      from dec01) as lnn order by line_number;

select line_number, case when lead(value) over () = '' then 0 else line_number end
from dec01;

select line_number, value, case when lead(value) over () = '' then '' else value end
from dec01;

select line_number, value, case when value is null then 0 else sum(value) over (order by line_number) end
from (select line_number, nullif(value, '')::int as value from dec01) as dec01a;

select line_number, value, case when value is null then -sum(sum(value) over (order by line_number)) over (order by line_number) else
    sum(value) over (order by line_number) end
from (select line_number, nullif(value, '')::int as value from dec01) as dec01a;

select line_number from (select line_number, value, case when value is null then -sum(value) else
    sum(value) over (order by line_number) end
from (select line_number, nullif(value, '')::int as value from dec01) as dec01a);
