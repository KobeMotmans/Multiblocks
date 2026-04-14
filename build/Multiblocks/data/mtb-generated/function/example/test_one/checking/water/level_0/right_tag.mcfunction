function mtb:find_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if score @s got_block matches 0 run return run function mtb-generated:example/test_one/checking/water/level_0/nb
execute if score @s got_block matches 1 run return run function mtb-generated:example/test_one/checking/water/level_0/wb
execute if score @s got_block matches 2 run return run function mtb-generated:example/test_one/checking/water/level_0/rb
