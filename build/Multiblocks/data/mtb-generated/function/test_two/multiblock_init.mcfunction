tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.0 ^-1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_0
execute positioned ^-1.0 ^-1.0 ^-1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_1
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.0 ^ summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_2
execute positioned ^-1.0 ^-1.0 ^ summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_3
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.0 ^1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_4
execute positioned ^-1.0 ^-1.0 ^1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_5
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.0 ^-1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_6
execute positioned ^ ^-1.0 ^-1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_7
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.0 ^ summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_8
execute positioned ^ ^-1.0 ^ summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_9
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.0 ^-1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_10
execute positioned ^1.0 ^-1.0 ^-1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_11
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^ ^ summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_12
execute positioned ^-1.0 ^ ^ summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_13
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^ ^1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_14
execute positioned ^-1.0 ^ ^1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_15
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-2.0 ^-1.0 summon minecraft:block_display run function mtb-generated:test_two/multiblock_init/nested_execute_16
execute positioned ^-1.0 ^-2.0 ^-1.0 summon block_display run function mtb-generated:test_two/multiblock_init/nested_execute_17
