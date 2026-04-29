function mtb-generated:example/test_three/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.example-test_three] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]
tp @s ^-2.0 ^ ^-2.0
rotate @s ~90 ~
execute at @s rotated as @s run tp @s ^2.0 ^ ^2.0
execute at @s rotated as @s run function mtb-generated:example/test_three/place_blueprint/summon
execute if @s[tag=mtb.has_outline] at @s rotated as @s run function #mtb-generated:mtb-generated:example/test_three/summon_outline
