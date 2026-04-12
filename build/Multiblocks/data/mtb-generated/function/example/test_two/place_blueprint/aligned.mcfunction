function mtb-generated:example/test_two/place_blueprint/handle_rotation
execute as @e[sort=nearest, limit=1, distance=0..0.1,type=marker,tag=example-test_two] at @s rotated as @s run function mtb-generated:example/test_two/summon with storage mtb-generated:example_test_two callback
