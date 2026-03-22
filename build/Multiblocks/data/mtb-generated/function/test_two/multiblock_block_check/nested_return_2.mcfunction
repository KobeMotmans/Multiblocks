scoreboard players set @s got_block 2
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "minecraft:dirt was placed", color: "green"}]
execute as @e[distance=0..5, type=marker, tag=test_two] run scoreboard players add @s mtb_complete 1
