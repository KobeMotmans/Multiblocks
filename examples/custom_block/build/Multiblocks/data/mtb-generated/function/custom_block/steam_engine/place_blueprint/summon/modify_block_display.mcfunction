$data merge entity @s {view_range:0.12f,transformation:{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]},block_state:$(display_data),Tags:["mtb.custom_block-steam_engine", "$(block_id)-$(blockstates)"]}
scoreboard players operation @s mtb_id = #root_id temp
scoreboard players set @s mtb_prev_state 0
tag @s add mtb.blueprint
execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 0 run tag @s add mtb.rot_0
execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 90 run tag @s add mtb.rot_90
execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 180 run tag @s add mtb.rot_180
execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 270 run tag @s add mtb.rot_270
execute unless entity @s[tag=mtb.has_rot_tag] if score #is_mirrored temp matches 1 run tag @s add mtb.mirrored
tag @s add mtb.has_rot_tag
