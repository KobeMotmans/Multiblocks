execute unless entity @s[type=marker, tag=example-test_one] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"Must run this command as the marker","color":"red"}
function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
execute as @s at @s rotated as @s run function mtb-generated:example/test_one/mirror_nested
