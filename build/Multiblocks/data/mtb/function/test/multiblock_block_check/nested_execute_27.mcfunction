execute if block ~ ~ ~ minecraft:air unless score @s got_block matches 0 run function mtb:test/multiblock_block_check/nested_execute_24
execute if block ~ ~ ~ minecraft:oak_fence_gate unless score @s got_block matches 2 run function mtb:test/multiblock_block_check/nested_execute_25
execute unless block ~ ~ ~ minecraft:oak_fence_gate unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1 run function mtb:test/multiblock_block_check/nested_execute_26
