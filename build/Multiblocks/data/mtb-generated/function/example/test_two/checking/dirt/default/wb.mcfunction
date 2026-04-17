execute if block ~ ~ ~ minecraft:dirt run return run function mtb-generated:example/test_two/checking/dirt/default/wb_to_rb
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:example/test_two/checking/dirt/default/wb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:dirt run return fail
