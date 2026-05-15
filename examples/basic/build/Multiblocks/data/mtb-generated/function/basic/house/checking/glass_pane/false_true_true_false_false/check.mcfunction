scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, west=true, east=true, south=false, north=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, north=true, south=true, west=false, east=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, east=true, west=true, north=false, south=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, south=true, north=true, east=false, west=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, east=true, west=true, south=false, north=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, south=true, north=true, west=false, east=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, west=true, east=true, north=false, south=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:glass_pane[waterlogged=false, north=true, south=true, east=false, west=false] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:glass_pane run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:basic/house/checking/glass_pane/false_true_true_false_false/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:basic/house/checking/glass_pane/false_true_true_false_false/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:basic/house/checking/glass_pane/false_true_true_false_false/set_correct
