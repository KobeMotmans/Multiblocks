execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Right block removed","color":"red"}]
execute as @e[predicate=mtb:match_id,type=marker,tag=example-test_two] run scoreboard players remove @s mtb_complete 1
scoreboard players set @s got_block 0
