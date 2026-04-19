function mtb-generated:example/test_four/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.example-test_four] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
execute as @s at @s rotated as @s run function mtb-generated:example/test_four/center_rotate_nested
