$data merge entity @s {view_range:0.12f,transformation:{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[0f,-0f,0f],scale:[0.6f,0.6f,0.6f]},item:$(display_data),Tags:["mtb.example-test_five", "$(block_id)"]}
scoreboard players operation @s mtb_id = #marker_id temp
scoreboard players set @s got_block 0
tag @s add mtb.rot_0
tag @s add mtb.blueprint
