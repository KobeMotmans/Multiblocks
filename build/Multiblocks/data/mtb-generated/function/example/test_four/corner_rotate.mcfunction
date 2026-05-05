function mtb-generated:example/test_four/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.example-test_four] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
tp @s ^-2.0 ^ ^-1.5
rotate @s ~90 ~
execute at @s rotated as @s run tp @s ^2.0 ^ ^1.5
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:example/test_four/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:example/test_four/outline/spawn_right_outline
