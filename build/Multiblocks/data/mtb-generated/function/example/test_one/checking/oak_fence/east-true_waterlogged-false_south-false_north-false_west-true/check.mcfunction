scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[east=true, waterlogged=false, south=false, north=false, west=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[south=true, waterlogged=false, west=false, east=false, north=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[west=true, waterlogged=false, north=false, south=false, east=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[north=true, waterlogged=false, east=false, west=false, south=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[west=true, waterlogged=false, south=false, north=false, east=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[north=true, waterlogged=false, west=false, east=false, south=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[east=true, waterlogged=false, north=false, south=false, west=true] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[south=true, waterlogged=false, east=false, west=false, north=true] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:oak_fence run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-false_north-false_west-true/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-false_north-false_west-true/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-false_north-false_west-true/set_correct
