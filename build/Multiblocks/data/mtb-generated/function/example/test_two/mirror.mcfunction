function mtb:find_id
scoreboard players set @e[limit=1,sort=nearest,type=marker,tag=test_two, predicate=mtb:match_id] mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
execute as @e[sort=nearest, type=marker, predicate=mtb:match_id, limit=1] at @s run function mirror_nested
scoreboard players set @p[sort=nearest, predicate=mtb:match_id, limit=1] mirror 0
