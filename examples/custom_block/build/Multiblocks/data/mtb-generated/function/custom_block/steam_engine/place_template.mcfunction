execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template custom_block:steam_engine ~2 ~ ~ none front_back
execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~5 clockwise_90 front_back
execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template custom_block:steam_engine ~-2 ~ ~ 180 front_back
execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~-5 counterclockwise_90 front_back
execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~ none
execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~ clockwise_90
execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~ 180
execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template custom_block:steam_engine ~ ~ ~ counterclockwise_90
