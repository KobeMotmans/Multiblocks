execute if block ~ ~ ~ minecraft:air unless score @s got_block matches 0 run function mtb-generated:test_two/multiblock_block_check/nested_execute_0
execute if block ~ ~ ~ minecraft:dirt unless score @s got_block matches 2 run function mtb-generated:test_two/multiblock_block_check/nested_execute_1
execute unless block ~ ~ ~ minecraft:dirt unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test_two/multiblock_block_check/nested_execute_2
