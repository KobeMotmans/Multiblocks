say ik ben mirrored
summon item_display ^ ^-1.5 ^ {transformation: {left_rotation: [0.0f, 0.0f, 0.0f, 1.0f], right_rotation: [0.0f, 0.0f, 0.0f, 1.0f], translation: [0.0f, 0.0f, 0.0f], scale: [0.6f, 0.6f, 0.6f]}, item: {id: "minecraft:water_bucket"}, Tags: ["test", "water"]}
execute positioned ^ ^-1.5 ^ run scoreboard players operation @e[distance=..0.1, type=item_display, tag=test, limit=1] mtb_id = @s mtb_id
