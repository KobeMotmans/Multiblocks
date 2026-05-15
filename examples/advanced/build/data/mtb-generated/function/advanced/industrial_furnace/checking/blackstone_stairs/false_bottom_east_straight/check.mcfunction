scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=east, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=south, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=west, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=north, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=west, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=north, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=east, shape=straight] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_stairs[waterlogged=false, half=bottom, facing=south, shape=straight] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:blackstone_stairs run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_stairs/false_bottom_east_straight/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_stairs/false_bottom_east_straight/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_stairs/false_bottom_east_straight/set_correct
