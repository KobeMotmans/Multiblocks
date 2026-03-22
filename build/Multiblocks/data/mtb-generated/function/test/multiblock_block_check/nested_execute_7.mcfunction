execute unless score @s got_block matches 0 unless block ~ ~ ~ minecraft:water run function mtb-generated:test/multiblock_block_check/nested_execute_4
execute if block ~ ~ ~ minecraft:water unless score @s got_block matches 2 run function mtb-generated:test/multiblock_block_check/nested_execute_5
execute unless block ~ ~ ~ minecraft:water unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test/multiblock_block_check/nested_execute_6
