execute unless function mtb-generated:basic/house/verify_marker run return fail
function mtb-generated:basic/house/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.basic-house] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:v0.1.2-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id]
execute at @s rotated as @s run function mtb-generated:basic/house/center_rotate_nested
