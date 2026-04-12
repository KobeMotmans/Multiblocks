execute if block ~ ~ ~ minecraft:oak_fence run return fail
execute if block ~ ~ ~ minecraft:air run return function mtb-generated:example/test_one/checking/oak_fence/east_false_waterlogged_false_south_true_north_true_west_false/rb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence run return function mtb-generated:example/test_one/checking/oak_fence/east_false_waterlogged_false_south_true_north_true_west_false/rb_to_wb
