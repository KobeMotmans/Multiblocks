scoreboard players enable @s mirror
scoreboard players enable @s rotate
execute at @e[distance=..10, type=marker, tag=rotor, tag=INIT, tag=test] align xyz positioned ~0.5 ~ ~0.5 run function mtb-generated:test/spawn_marker
execute as @e[distance=..10, type=#mtb:display, tag=test] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb-generated:test/multiblock_block_check
execute as @e[distance=..10, type=marker, tag=test] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb-generated:test/multiblock_check
execute at @e[distance=..10, type=marker, tag=rotor, tag=INIT, tag=test_two] align xyz positioned ~0.5 ~ ~0.5 run function mtb-generated:test_two/spawn_marker
execute as @e[distance=..10, type=#mtb:display, tag=test_two] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb-generated:test_two/multiblock_block_check
execute as @e[distance=..10, type=marker, tag=test_two] at @s align xyz positioned ~0.5 ~0.5 ~0.5 run function mtb-generated:test_two/multiblock_check
