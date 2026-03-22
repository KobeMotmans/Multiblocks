execute unless score @s got_block matches 0 unless block ~ ~ ~ minecraft:oak_fence run function mtb-generated:test/multiblock_block_check/nested_execute_16
execute if block ~ ~ ~ minecraft:oak_fence unless score @s got_block matches 2 run function mtb-generated:test/multiblock_block_check/nested_execute_17
execute unless block ~ ~ ~ minecraft:oak_fence unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb-generated:test/multiblock_block_check/nested_execute_18
