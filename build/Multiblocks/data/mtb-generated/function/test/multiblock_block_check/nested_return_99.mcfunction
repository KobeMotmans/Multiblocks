execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Ik heb geen blok", color: "red"}]
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:test/multiblock_block_check/nested_return_96
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:oak_fence run return run function mtb-generated:test/multiblock_block_check/nested_return_97
execute if block ~ ~ ~ minecraft:oak_fence run return run function mtb-generated:test/multiblock_block_check/nested_return_98
