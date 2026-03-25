tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
$$(on_place)
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-1.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_0
execute positioned ^-2.0 ^-1.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_1
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-1.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_2
execute positioned ^-2.0 ^-1.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_3
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-1.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_4
execute positioned ^-2.0 ^-1.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_5
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-1.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_6
execute positioned ^-2.0 ^-1.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_7
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-1.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_8
execute positioned ^-2.0 ^-1.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_9
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_10
execute positioned ^-1.0 ^-1.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_11
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_12
execute positioned ^-1.0 ^-1.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_13
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_14
execute positioned ^-1.0 ^-1.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_15
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_16
execute positioned ^-1.0 ^-1.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_17
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-1.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_18
execute positioned ^-1.0 ^-1.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_19
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_20
execute positioned ^ ^-1.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_21
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_22
execute positioned ^ ^-1.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_23
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_24
execute positioned ^ ^-1.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_25
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-1.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_26
execute positioned ^ ^-1.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_27
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_28
execute positioned ^1.0 ^-1.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_29
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_30
execute positioned ^1.0 ^-1.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_31
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_32
execute positioned ^1.0 ^-1.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_33
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_34
execute positioned ^1.0 ^-1.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_35
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-1.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_36
execute positioned ^1.0 ^-1.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_37
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-1.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_38
execute positioned ^2.0 ^-1.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_39
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-1.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_40
execute positioned ^2.0 ^-1.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_41
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-1.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_42
execute positioned ^2.0 ^-1.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_43
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-1.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_44
execute positioned ^2.0 ^-1.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_45
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-1.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_46
execute positioned ^2.0 ^-1.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_47
scoreboard players operation #marker_id temp = @s mtb_id
execute unless entity @s[tag=mirrored] positioned ^ ^-1.5 ^ summon item_display run function mtb-generated:test_one/multiblock_init/nested_execute_48
execute if entity @s[tag=mirrored] positioned ^ ^-1.5 ^ summon item_display run function mtb-generated:test_one/multiblock_init/nested_execute_49
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-0.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_50
execute positioned ^-2.0 ^-0.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_51
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-0.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_52
execute positioned ^-2.0 ^-0.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_53
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-0.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_54
execute positioned ^-2.0 ^-0.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_55
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-0.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_56
execute positioned ^-2.0 ^-0.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_57
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^2.0 ^-0.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_58
execute positioned ^-2.0 ^-0.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_59
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-0.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_60
execute positioned ^-1.0 ^-0.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_61
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^1.0 ^-0.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_62
execute positioned ^-1.0 ^-0.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_63
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-0.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_64
execute positioned ^ ^-0.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_65
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^ ^-0.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_66
execute positioned ^ ^-0.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_67
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-0.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_68
execute positioned ^1.0 ^-0.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_69
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-1.0 ^-0.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_70
execute positioned ^1.0 ^-0.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_71
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-0.5 ^-2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_72
execute positioned ^2.0 ^-0.5 ^-2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_73
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-0.5 ^-1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_74
execute positioned ^2.0 ^-0.5 ^-1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_75
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-0.5 ^ summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_76
execute positioned ^2.0 ^-0.5 ^ summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_77
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-0.5 ^1.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_78
execute positioned ^2.0 ^-0.5 ^1.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_79
scoreboard players operation #marker_id temp = @s mtb_id
execute if entity @s[tag=mirrored] run return run execute positioned ^-2.0 ^-0.5 ^2.0 summon minecraft:block_display run function mtb-generated:test_one/multiblock_init/nested_execute_80
execute positioned ^2.0 ^-0.5 ^2.0 summon block_display run function mtb-generated:test_one/multiblock_init/nested_execute_81
