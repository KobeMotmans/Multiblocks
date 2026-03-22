execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Ik heb geen blok", color: "red"}]
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:test/multiblock_block_check/nested_return_72
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence_gate run return run function mtb-generated:test/multiblock_block_check/nested_return_73
execute if block ~ ~ ~ minecraft:oak_fence_gate run return run function mtb-generated:test/multiblock_block_check/nested_return_74
