kill @e[distance=..0.1,type=item_display,tag=outline]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Wrong block removed","color":"gold"}]
scoreboard players set @s got_block 0
