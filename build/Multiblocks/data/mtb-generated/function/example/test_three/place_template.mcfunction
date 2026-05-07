execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template example:test_three ~4 ~ ~ none front_back
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template example:test_three ~ ~ ~5 clockwise_90 front_back
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template example:test_three ~-4 ~ ~ 180 front_back
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template example:test_three ~ ~ ~-5 counterclockwise_90 front_back
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template example:test_three ~ ~ ~ none
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template example:test_three ~ ~ ~ clockwise_90
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template example:test_three ~ ~ ~ 180
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template example:test_three ~ ~ ~ counterclockwise_90
