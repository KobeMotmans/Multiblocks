execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template basic:house ~6 ~ ~ none front_back
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template basic:house ~ ~ ~9 clockwise_90 front_back
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template basic:house ~-6 ~ ~ 180 front_back
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template basic:house ~ ~ ~-9 counterclockwise_90 front_back
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template basic:house ~ ~ ~ none
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template basic:house ~ ~ ~ clockwise_90
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template basic:house ~ ~ ~ 180
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template basic:house ~ ~ ~ counterclockwise_90
