execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Right block was switched with wrong block", color: "red"}]
scoreboard players set @s got_block 1
summon item_display ~ ~ ~ {item: {id: "minecraft:poisonous_potato", count: 1, components: {"minecraft:item_model": "minecraft:red_stained_glass"}}, Tags: ["outline"]}
execute as @e[distance=0..5, type=marker, tag=test_two] run scoreboard players remove @s mtb_complete 1
