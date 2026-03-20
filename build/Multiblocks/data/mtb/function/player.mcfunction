execute as @s at @e[distance=(0,10),type=marker,tag=rotor, tag=INIT] align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:test/spawn_marker
execute as @e[distance=(0,10),type=minecraft:block_display,tag=test] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:test/multiblock_block_check
execute as @e[distance=(0,10),type=marker,tag=test] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:test/multiblock_check_
