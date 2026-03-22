data merge entity @s {transformation: {left_rotation: [0.0f, 0.0f, 0.0f, 1.0f], right_rotation: [0.0f, 0.0f, 0.0f, 1.0f], translation: [-0.3f, -0.3f, -0.3f], scale: [0.6f, 0.6f, 0.6f]}, block_state: {Name: "minecraft:oak_fence_gate"}, Tags: ["test", "oak_fence_gate"]}
scoreboard players operation @s mtb_id = #marker_id temp
scoreboard players set @s got_block 0
