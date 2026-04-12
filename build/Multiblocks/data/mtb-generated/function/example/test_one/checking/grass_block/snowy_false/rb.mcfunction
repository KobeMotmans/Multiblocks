execute if block ~ ~ ~ minecraft:grass_block run return fail
execute if block ~ ~ ~ minecraft:air run return function mtb-generated:example/test_one/checking/grass_block/snowy_false/rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:grass_block run return function mtb-generated:example/test_one/checking/grass_block/snowy_false/rb_to_wb
