scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[east=true, waterlogged=false, south=true, north=false, west=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[south=true, waterlogged=false, west=true, east=false, north=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[west=true, waterlogged=false, north=true, south=false, east=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[north=true, waterlogged=false, east=true, west=false, south=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[west=true, waterlogged=false, south=true, north=false, east=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[north=true, waterlogged=false, west=true, east=false, south=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[east=true, waterlogged=false, north=true, south=false, west=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence[south=true, waterlogged=false, east=true, west=false, north=false] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:oak_fence run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-true_north-false_west-false/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-true_north-false_west-false/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:example/test_one/checking/oak_fence/east-true_waterlogged-false_south-true_north-false_west-false/set_correct
