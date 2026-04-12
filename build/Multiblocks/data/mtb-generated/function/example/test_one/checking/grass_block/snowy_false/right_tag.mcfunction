function mtb:find_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if score @s got_block matches 0 run return function mtb-generated:example/test_one/checking/grass_block/snowy_false/nb
execute if score @s got_block matches 1 run return function mtb-generated:example/test_one/checking/grass_block/snowy_false/wb
execute if score @s got_block matches 2 run return function mtb-generated:example/test_one/checking/grass_block/snowy_false/rb
