execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Wrong block was placed","color":"red"}]
scoreboard players set @s got_block 1
execute at @s summon item_display run function mtb-generated:example/test_one/checking/oak_fence/east_false_waterlogged_false_south_false_north_true_west_true/nb_to_wb_nested
