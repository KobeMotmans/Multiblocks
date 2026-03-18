execute if entity @s[tag=INIT] run tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
scoreboard players operation @e[type=interaction, tag=test_two, tag=INIT, sort=nearest, limit=1] mtb_id = @s mtb_id
execute as @e[type=interaction, tag=test_two, tag=INIT, limit=1] run tag @s remove INIT
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_0
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_1
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_2
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_3
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_4
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_5
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_6
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_7
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_8
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_9
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_10
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_11
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_12
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_13
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_14
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_15
execute unless entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_16
execute if entity @s[tag=mirrored] run function mtb:test_two/multiblock_init/nested_execute_17
