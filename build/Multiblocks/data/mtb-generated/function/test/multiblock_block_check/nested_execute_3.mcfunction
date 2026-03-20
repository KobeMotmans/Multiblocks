execute unless score @s got_block matches 0 if block ~ ~ ~ minecraft:air run function mtb-generated:test/multiblock_block_check/nested_execute_0
execute if block ~ ~ ~ minecraft:grass_block unless score @s got_block matches 2 run function mtb-generated:test/multiblock_block_check/nested_execute_1
execute unless block ~ ~ ~ minecraft:grass_block unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test/multiblock_block_check/nested_execute_2
