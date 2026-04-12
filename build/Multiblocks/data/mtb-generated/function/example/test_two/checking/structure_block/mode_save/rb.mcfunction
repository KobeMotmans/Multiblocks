execute if block ~ ~ ~ minecraft:structure_block run return fail
execute if block ~ ~ ~ minecraft:air run return function mtb-generated:example/test_two/checking/structure_block/mode_save/rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:structure_block run return function mtb-generated:example/test_two/checking/structure_block/mode_save/rb_to_wb
