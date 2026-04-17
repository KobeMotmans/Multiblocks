execute if block ~ ~ ~ minecraft:oak_fence_gate run return run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall_false_powered_false_facing_south_open_false/wb_to_rb
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall_false_powered_false_facing_south_open_false/wb_to_nb
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence_gate run return fail
