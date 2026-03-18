execute if block ~ ~ ~ minecraft:air unless score @s got_block matches 0 run function mtb:test/multiblock_block_check/nested_execute_28
execute if block ~ ~ ~ minecraft:oak_fence unless score @s got_block matches 2 run function mtb:test/multiblock_block_check/nested_execute_29
execute unless block ~ ~ ~ minecraft:oak_fence unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb:test/multiblock_block_check/nested_execute_30
