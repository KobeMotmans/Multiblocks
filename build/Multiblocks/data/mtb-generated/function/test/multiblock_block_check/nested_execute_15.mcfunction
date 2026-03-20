execute unless score @s got_block matches 0 if block ~ ~ ~ minecraft:air run function mtb-generated:test/multiblock_block_check/nested_execute_12
execute if block ~ ~ ~ minecraft:oak_fence unless score @s got_block matches 2 run function mtb-generated:test/multiblock_block_check/nested_execute_13
execute unless block ~ ~ ~ minecraft:oak_fence unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test/multiblock_block_check/nested_execute_14
