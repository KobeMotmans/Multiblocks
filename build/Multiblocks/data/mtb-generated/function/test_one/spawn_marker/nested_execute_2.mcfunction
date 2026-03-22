function mtb-generated:test_one/spawn_marker/nested_execute_0
kill @e[sort=nearest, limit=1, distance=0..1, type=marker, tag=rotor, tag=INIT]
execute as @e[sort=nearest, limit=1, distance=0..0.1, type=marker, tag=test_one, tag=INIT] at @s rotated as @s run function mtb-generated:test_one/spawn_marker/nested_execute_1
