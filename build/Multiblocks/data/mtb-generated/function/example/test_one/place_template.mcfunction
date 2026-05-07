execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template example:test_four ~4 ~ ~ none front_back
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template example:test_four ~ ~ ~4 clockwise_90 front_back
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template example:test_four ~-4 ~ ~ 180 front_back
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template example:test_four ~ ~ ~-4 counterclockwise_90 front_back
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template example:test_four ~ ~ ~ none
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template example:test_four ~ ~ ~ clockwise_90
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template example:test_four ~ ~ ~ 180
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template example:test_four ~ ~ ~ counterclockwise_90
