scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, west=false, east=true, south=false, north=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, north=false, south=true, west=false, east=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, east=false, west=true, north=false, south=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, south=false, north=true, east=false, west=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, east=false, west=true, south=false, north=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, south=false, north=true, west=false, east=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, west=false, east=true, north=false, south=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[waterlogged=false, north=false, south=true, east=false, west=true] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:oak_fence run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:basic/house/checking/oak_fence/false_false_true_false_true/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:basic/house/checking/oak_fence/false_false_true_false_true/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:basic/house/checking/oak_fence/false_false_true_false_true/set_correct
