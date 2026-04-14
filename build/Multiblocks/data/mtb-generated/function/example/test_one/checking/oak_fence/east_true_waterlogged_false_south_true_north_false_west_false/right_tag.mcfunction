function mtb:find_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if score @s got_block matches 0 run return run function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_true_north_false_west_false/nb
execute if score @s got_block matches 1 run return run function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_true_north_false_west_false/wb
execute if score @s got_block matches 2 run return run function mtb-generated:example/test_one/checking/oak_fence/east_true_waterlogged_false_south_true_north_false_west_false/rb
