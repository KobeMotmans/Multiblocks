scoreboard players set @e[limit=1, distance=0..10, type=marker, tag=test] mtb_complete 0
kill @e[distance=..10, type=minecraft:block_display, predicate=mtb:match_id]
execute as @e[distance=..10, type=marker, predicate=mtb:match_id, limit=1] at @s run function mtb:test/interaction/nested_execute_3
scoreboard players set @p[distance=..10, predicate=mtb:match_id, limit=1] mirror 0
