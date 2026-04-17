function mtb-generated:example/test_one/place_blueprint/handle_rotation
execute as @e[type=marker, sort=nearest, limit=1, tag=example-test_one, tag=INIT, distance=..0.1] at @s rotated as @s run function mtb-generated:example/test_one/pre_summon
