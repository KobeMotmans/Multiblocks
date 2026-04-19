scoreboard players set #success temp 0
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=south, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=west, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=north, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=east, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=south, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=west, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=north, open=false] run scoreboard players set #success temp 2
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ minecraft:oak_fence_gate[in_wall=false, powered=false, facing=east, open=false] run scoreboard players set #success temp 2
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:oak_fence_gate run scoreboard players set #success temp 1
execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall-false_powered-false_facing-south_open-false/set_none
execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall-false_powered-false_facing-south_open-false/set_wrong
execute unless score @s mtb_prev_state matches 2 run function mtb-generated:example/test_one/checking/oak_fence_gate/in_wall-false_powered-false_facing-south_open-false/set_correct
