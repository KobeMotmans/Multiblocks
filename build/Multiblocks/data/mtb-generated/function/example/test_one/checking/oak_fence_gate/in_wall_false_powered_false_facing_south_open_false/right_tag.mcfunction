function mtb:find_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if score @s got_block matches 0 run return run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall_false_powered_false_facing_south_open_false/nb
execute if score @s got_block matches 1 run return run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall_false_powered_false_facing_south_open_false/wb
execute if score @s got_block matches 2 run return run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall_false_powered_false_facing_south_open_false/rb
