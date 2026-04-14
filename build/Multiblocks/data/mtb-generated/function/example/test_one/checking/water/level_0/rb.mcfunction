execute if block ~ ~ ~ minecraft:water run return fail
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:example/test_one/checking/water/level_0/rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:water run return run function mtb-generated:example/test_one/checking/water/level_0/rb_to_wb
