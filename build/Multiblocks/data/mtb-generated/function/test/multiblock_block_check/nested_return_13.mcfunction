execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Wrong block was placed", color: "red"}]
scoreboard players set @s got_block 1
summon item_display ~ ~ ~ {item: {id: "minecraft:poisonous_potato", count: 1, components: {"minecraft:item_model": "minecraft:red_stained_glass"}}, Tags: ["outline"], transformation: {left_rotation: [0.0f, 0.0f, 0.0f, 1.0f], right_rotation: [0.0f, 0.0f, 0.0f, 1.0f], translation: [0.0f, 0.0f, 0.0f], scale: [1.01f, 1.01f, 1.01f]}}
