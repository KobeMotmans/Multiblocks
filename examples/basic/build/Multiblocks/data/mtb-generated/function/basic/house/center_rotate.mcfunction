execute unless function mtb-generated:basic/house/verify_root run return fail
function mtb-generated:basic/house/rot/find_rot
function mtb:v0.1.2-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id, tag=!mtb.root]
execute at @s rotated as @s run function mtb-generated:basic/house/center_rotate_nested

