execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Right block was switched with wrong block","color":"red"}]
scoreboard players set @s got_block 1
execute at @s summon item_display run function mtb-generated:example/test_one/checking/water/level_0/rb_to_wb_nested
execute as @e[predicate=mtb:match_id,type=marker,tag=test_one] run scoreboard players remove @s mtb_complete 1
