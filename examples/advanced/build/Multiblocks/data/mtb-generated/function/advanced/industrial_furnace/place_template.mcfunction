execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template advanced:industrial_furnace ~2 ~ ~ none front_back
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~3 clockwise_90 front_back
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template advanced:industrial_furnace ~-2 ~ ~ 180 front_back
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~-3 counterclockwise_90 front_back
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~ none
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~ clockwise_90
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~ 180
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template advanced:industrial_furnace ~ ~ ~ counterclockwise_90
