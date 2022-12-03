DROP TABLE IF EXISTS dec03;

CREATE UNLOGGED TABLE dec03
(
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    row_data    text   NOT NULL
);

COPY dec03 (row_data) FROM '/aoc/days/day_03/input.txt';
-- COPY dec03 (row_data) FROM '/aoc/days/day_03/test_input.txt';
-- VACUUM ANALYZE dec03;

-- SELECT length(row_data)
-- from dec03;
--
-- SELECT row_data,
--        substring(row_data, 1, length(row_data) / 2),
--        substring(row_data, length(row_data) / 2 + 1, length(row_data))
-- from dec03;
--
-- SELECT unnest(string_to_array(substring(row_data, 1, length(row_data) / 2), ''))
-- from dec03;
--
-- select ascii('a'),
--        ascii('A'),
--        ascii('A') - 38,
--        ascii('a') - 96,
--        ascii('Z') - 38,
--        ascii('z') - 96,
--        ascii('s'),
--        ascii('s') - 96;

SELECT line_number,
       unnest(string_to_array(row_data, null)) as letter,
       (line_number - 1) / 3                   as e_group
from dec03
order by line_number;

with e1 as (SELECT line_number,
                   unnest(string_to_array(row_data, null)) as letter,
--                    row_data as letter,
                   (line_number - 1) / 3                   as e_group
            from dec03
            where line_number % 3 = 1
            order by line_number),
     e2 as (SELECT line_number,
                   unnest(string_to_array(row_data, null)) as letter,
--                    row_data as letter,
                   (line_number - 1) / 3                   as e_group
            from dec03
            where line_number % 3 = 2
            order by line_number),
     e3 as (SELECT line_number,
                   unnest(string_to_array(row_data, null)) as letter,
--                    row_data as letter,
                   (line_number - 1) / 3                   as e_group
            from dec03
            where line_number % 3 = 0
            order by line_number),
    res_letters as (
select distinct e1.line_number, e1.letter, ascii(e1.letter) as l_num, e1.e_group
from e1
         join e2 on e1.e_group = e2.e_group and e1.letter = e2.letter
         join e3 on e1.e_group = e3.e_group and e1.letter = e3.letter),
     priorities as (select line_number,
                           letter,
                           l_num,
                           case
                               when l_num < 97 then l_num - 38
                               when l_num > 65 then l_num - 96
                               end priority
                    from res_letters)
select sum(priority)
from priorities;

