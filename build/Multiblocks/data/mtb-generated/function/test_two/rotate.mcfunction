scoreboard players set @e[limit=1, sort=nearest, type=marker, tag=test_two, predicate=mtb:match_id] mtb_complete 0
kill @e[sort=nearest, type=minecraft:block_display, predicate=mtb:match_id]
kill @e[sort=nearest, type=minecraft:item_display, predicate=mtb:match_id]
execute as @e[sort=nearest, type=marker, predicate=mtb:match_id, limit=1] at @s run function mtb-generated:test_two/rotate/nested_execute_0
scoreboard players set @p[sort=nearest, predicate=mtb:match_id, limit=1] rotate 0
