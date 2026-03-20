execute if score @s got_block matches 2 run execute as @e[distance=0..5, type=marker, tag=test_two] run scoreboard players remove @s mtb_complete 1
scoreboard players set @s got_block 0
kill @e[distance=..0.1, type=item_display, tag=outline]
