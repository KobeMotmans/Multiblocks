scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, west=none, east=none, south=none, north=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, north=none, south=none, west=none, east=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, east=none, west=none, north=none, south=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, south=none, north=none, east=none, west=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, east=none, west=none, south=none, north=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, south=none, north=none, west=none, east=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, west=none, east=none, north=none, south=none] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:blackstone_wall[waterlogged=false, up=true, north=none, south=none, east=none, west=none] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:blackstone_wall run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_wall/false_true_none_none_none_none/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_wall/false_true_none_none_none_none/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:advanced/industrial_furnace/checking/blackstone_wall/false_true_none_none_none_none/set_correct
