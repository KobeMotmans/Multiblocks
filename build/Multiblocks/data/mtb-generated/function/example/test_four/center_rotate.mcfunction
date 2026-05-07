execute unless function mtb-generated:example/test_four/verify_marker run return fail
function mtb-generated:example/test_four/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.example-test_four] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:v0.1-alpha/find_id
scoreboard players set @s mtb_complete 0
execute at @s run tp @s ^0.5 ^ ^0.5
kill @e[sort=nearest, type=#mtb:v0.1-alpha/display, predicate=mtb:v0.1-alpha/match_id]
execute as @s at @s rotated as @s run function mtb-generated:example/test_four/center_rotate_nested
