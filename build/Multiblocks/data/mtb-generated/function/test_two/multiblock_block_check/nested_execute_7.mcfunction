execute if block ~ ~ ~ minecraft:air unless score @s got_block matches 0 run function mtb-generated:test_two/multiblock_block_check/nested_execute_4
execute if block ~ ~ ~ minecraft:structure_block unless score @s got_block matches 2 run function mtb-generated:test_two/multiblock_block_check/nested_execute_5
execute unless block ~ ~ ~ minecraft:structure_block unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test_two/multiblock_block_check/nested_execute_6
