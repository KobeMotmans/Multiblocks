function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
tp @s ^-2.0 ^ ^-2.0
particle minecraft:angry_villager
rotate @s ~90 ~
execute at @s rotated as @s run tp @s ^2.0 ^ ^2.0
particle minecraft:happy_villager
execute at @s rotated as @s run function mtb-generated:example/test_one/summon
