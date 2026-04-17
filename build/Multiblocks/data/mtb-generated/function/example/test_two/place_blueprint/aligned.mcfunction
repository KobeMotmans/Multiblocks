function mtb-generated:example/test_two/place_blueprint/handle_rotation
execute as @e[type=marker, sort=nearest, limit=1, tag=example-test_two, tag=INIT, distance=..0.1] at @s rotated as @s run function mtb-generated:example/test_two/pre_summon
