execute if block ~ ~ ~ minecraft:dirt run return fail
execute if block ~ ~ ~ minecraft:air run return function mtb-generated:example/test_two/checking/dirt//rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:dirt run return function mtb-generated:example/test_two/checking/dirt//rb_to_wb
