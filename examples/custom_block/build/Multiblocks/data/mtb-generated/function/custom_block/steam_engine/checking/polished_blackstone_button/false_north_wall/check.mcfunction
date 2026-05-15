scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=north, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=east, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=south, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=west, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=north, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=east, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=south, face=wall] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:polished_blackstone_button[powered=false, facing=west, face=wall] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:polished_blackstone_button run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:custom_block/steam_engine/checking/polished_blackstone_button/false_north_wall/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:custom_block/steam_engine/checking/polished_blackstone_button/false_north_wall/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:custom_block/steam_engine/checking/polished_blackstone_button/false_north_wall/set_correct
