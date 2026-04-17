kill @e[distance=..0.1,type=item_display,tag=outline]
scoreboard players set @s got_block 2
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"minecraft:oak_fence_gate was placed","color":"green"}]
execute as @e[predicate=mtb:match_id,type=marker,tag=example-test_one] run scoreboard players add @s mtb_complete 1
