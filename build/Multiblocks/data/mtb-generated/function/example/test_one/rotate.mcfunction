function mtb:find_id
particle minecraft:angry_villager
scoreboard players set @e[limit=1,sort=nearest,type=marker,tag=test_one, predicate=mtb:match_id] mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
execute as @e[sort=nearest, type=marker, predicate=mtb:match_id, limit=1] at @s run function mtb-generated:example/test_one/rotate_nested
scoreboard players set @p[sort=nearest, predicate=mtb:match_id, limit=1] rotate 0
