$data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]},item:{id:"$(block_state)"},block_state:{Name:"$(block_state)"},Tags:["example-test_two", "$(block_id)"]}
scoreboard players operation @s mtb_id = #marker_id temp
scoreboard players set @s got_block 0
