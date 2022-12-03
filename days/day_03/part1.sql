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

with p1 as (SELECT line_number,
                   unnest(string_to_array(substring(row_data, 1, length(row_data) / 2), null)) as letter,
                   1                                                                           as pocket
            from dec03
            order by line_number),
     p2 as (SELECT line_number,
                   unnest(string_to_array(substring(row_data, length(row_data) / 2 + 1, length(row_data)),
                                          null)) as letter,
                   2                             as pocket
            from dec03
            order by line_number),
     res_letters as (select distinct p1.line_number, p1.letter, ascii(p1.letter) as l_num, p1.pocket
                     from p1
                              join p2 on p1.line_number = p2.line_number and p1.letter = p2.letter),
    priorities as (
    select line_number, letter, l_num, pocket, case
    when l_num < 97 then l_num - 38
    when l_num > 65 then l_num - 96
    end priority
    from res_letters)

select sum(priority)
from priorities;

