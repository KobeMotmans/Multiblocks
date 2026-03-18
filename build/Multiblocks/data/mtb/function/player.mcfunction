scoreboard players enable @s mirror
scoreboard players enable @s rotate
execute as @s at @e[distance=0..10, type=marker, tag=rotor, tag=INIT, tag=test] align xyz positioned ~0.5 ~ ~0.5 run function mtb:test/spawn_marker
execute as @e[distance=0..10, type=minecraft:block_display, tag=test] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb:test/multiblock_block_check
execute as @e[distance=0..10, type=marker, tag=test] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb:test/multiblock_check
execute as @s at @e[distance=0..10, type=marker, tag=rotor, tag=INIT, tag=test_two] align xyz positioned ~0.5 ~ ~0.5 run function mtb:test_two/spawn_marker
execute as @e[distance=0..10, type=minecraft:block_display, tag=test_two] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb:test_two/multiblock_block_check
execute as @e[distance=0..10, type=marker, tag=test_two] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb:test_two/multiblock_check
