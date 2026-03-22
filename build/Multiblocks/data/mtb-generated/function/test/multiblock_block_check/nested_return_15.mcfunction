execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{text: "Ik heb geen blok", color: "red"}]
execute if block ~ ~ ~ minecraft:air run return run function mtb-generated:test/multiblock_block_check/nested_return_12
execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ minecraft:water run return run function mtb-generated:test/multiblock_block_check/nested_return_13
execute if block ~ ~ ~ minecraft:water run return run function mtb-generated:test/multiblock_block_check/nested_return_14
