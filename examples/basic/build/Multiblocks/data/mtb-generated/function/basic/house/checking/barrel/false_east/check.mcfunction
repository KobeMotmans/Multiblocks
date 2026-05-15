scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=east] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=south] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=west] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=north] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=west] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=north] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=east] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:barrel[open=false, facing=south] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:barrel run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:basic/house/checking/barrel/false_east/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:basic/house/checking/barrel/false_east/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:basic/house/checking/barrel/false_east/set_correct
