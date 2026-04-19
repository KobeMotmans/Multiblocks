scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=south, shape=outer_right] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=west, shape=outer_right] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=north, shape=outer_right] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=east, shape=outer_right] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=south, shape=outer_left] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=west, shape=outer_left] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=north, shape=outer_left] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:spruce_stairs[waterlogged=false, half=bottom, facing=east, shape=outer_left] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:spruce_stairs run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:example/test_three/checking/spruce_stairs/waterlogged-false_half-bottom_facing-south_shape-outer_right/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:example/test_three/checking/spruce_stairs/waterlogged-false_half-bottom_facing-south_shape-outer_right/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:example/test_three/checking/spruce_stairs/waterlogged-false_half-bottom_facing-south_shape-outer_right/set_correct
