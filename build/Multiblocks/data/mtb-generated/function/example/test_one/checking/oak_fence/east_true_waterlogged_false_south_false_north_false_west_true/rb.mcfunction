execute if block ~ ~ ~ minecraft:oak_fence run return fail
execute if block ~ ~ ~ minecraft:air run return function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_false_north_false_west_true/rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence run return function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_false_north_false_west_true/rb_to_wb
