function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
execute as @s at @s rotated as @s run function mtb-generated:example/test_one/mirror_nested
