execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Ik heb geen blok", color: "red"}]
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:test/multiblock_block_check/nested_return_0
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:grass_block run return run function mtb-generated:test/multiblock_block_check/nested_return_1
execute if block ~ ~ ~ minecraft:grass_block run return run function mtb-generated:test/multiblock_block_check/nested_return_2
