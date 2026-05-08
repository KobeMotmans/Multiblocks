execute unless function mtb-generated:example/test_five/verify_marker run return fail
function mtb:v0.1-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[type=#mtb:v0.1-alpha/display, predicate=mtb:v0.1-alpha/match_id]
execute as @s at @s rotated as @s run function mtb-generated:example/test_five/mirror_nested
