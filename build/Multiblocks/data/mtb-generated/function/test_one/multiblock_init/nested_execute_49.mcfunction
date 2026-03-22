data merge entity @s {transformation: {left_rotation: [0.0f, 0.0f, 0.0f, 1.0f], right_rotation: [0.0f, 0.0f, 0.0f, 1.0f], translation: [0.0f, 0.0f, 0.0f], scale: [0.6f, 0.6f, 0.6f]}, item: {id: "minecraft:water_bucket"}, Tags: ["test_one", "water"]}
scoreboard players operation @s mtb_id = #marker_id temp
scoreboard players set @s got_block 0
