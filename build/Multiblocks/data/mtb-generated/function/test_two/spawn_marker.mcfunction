execute if entity @s[y_rotation=135..225] run summon marker ~ ~ ~ {Rotation: [180.0f, 0.0f], Tags: ["test_two", "INIT"]}
execute if entity @s[y_rotation=225..315] run summon marker ~ ~ ~ {Rotation: [270.0f, 0.0f], Tags: ["test_two", "INIT"]}
execute if entity @s[y_rotation=315..] run summon marker ~ ~ ~ {Rotation: [0.0f, 0.0f], Tags: ["test_two", "INIT"]}
execute if entity @s[y_rotation=..45] run summon marker ~ ~ ~ {Rotation: [0.0f, 0.0f], Tags: ["test_two", "INIT"]}
execute if entity @s[y_rotation=45..135] run summon marker ~ ~ ~ {Rotation: [90.0f, 0.0f], Tags: ["test_two", "INIT"]}
summon interaction ~ ~ ~ {Tags: ["test_two", "INIT"]}
kill @e[sort=nearest, limit=1, distance=0..1, type=marker, tag=rotor, tag=INIT]
execute as @e[sort=nearest, limit=1, distance=0..0.1, type=marker, tag=test_two, tag=INIT] at @s rotated as @s run function mtb-generated:test_two/spawn_marker/nested_execute_0
