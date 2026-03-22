scoreboard players set @s got_block 2
kill @e[distance=..0.1, type=item_display, tag=outline]
execute as @e[distance=0..5, type=marker, tag=test_two] run scoreboard players add @s mtb_complete 1
