execute if entity @s[y_rotation=135..225] run summon marker ~ ~ ~ {Rotation:[180f,0f], Tags:[mtb,INIT]}
execute if entity @s[y_rotation=225..315] run summon marker ~ ~ ~ {Rotation:[270f,0f], Tags:[mtb,INIT]}
execute if entity @s[y_rotation=315..] run summon marker ~ ~ ~ {Rotation:[0f,0f], Tags:[mtb,INIT]}
execute if entity @s[y_rotation=..45] run summon marker ~ ~ ~ {Rotation:[0f,0f], Tags:[mtb,INIT]}
execute if entity @s[y_rotation=45..135] run summon marker ~ ~ ~ {Rotation:[90f,0f], Tags:[mtb,INIT]}
execute as @e[distance=(0,0.1),type=marker,tag=test, tag=INIT] at @s rotated as @s run function mtb:test/multiblock_init
kill @e[distance=(0,1),type=marker,tag=rotor, tag=INIT]
