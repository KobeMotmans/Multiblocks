execute if block ~ ~ ~ minecraft:oak_fence run return run function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_true_north_false_west_false/wb_to_rb
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_true_north_false_west_false/wb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence run return fail
