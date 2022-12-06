DROP TABLE IF EXISTS dec06;

CREATE UNLOGGED TABLE dec06
(
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data    text   NOT NULL
);

COPY dec06 (row_data) FROM '/aoc/days/day_06/input.txt';
-- COPY dec06 (row_data) FROM '/aoc/days/day_06/test_input.txt';

with letters as (SELECT row_data,
                        a.elem as letter,
                        a.nr   as row_number
                 from dec06,
                      unnest(string_to_array(row_data, null)) with ordinality as a(elem, nr)),
     windows as (select letter,
                        row_number,
                        array_to_string(array_agg(letter)
                                        OVER (ORDER BY row_number ROWS BETWEEN 13 PRECEDING AND CURRENT ROW),
                                        '') as roll_substr
                 from letters),
     hists as (select distinct regexp_split_to_table(roll_substr, '') as lets,
                               row_number,
                               bool_or(length(roll_substr) = 14)       as len_good,
                               count(*)                               as let_hist
               from windows
               group by row_number, lets
               order by row_number),
     max_hist as (select row_number, max(let_hist) as max_h
                  from hists
                  where len_good
                  group by row_number)
select min(row_number)
from max_hist
where max_h = 1;
