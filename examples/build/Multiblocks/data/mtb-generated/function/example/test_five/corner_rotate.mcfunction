function mtb-generated:example/test_five/rot/find_rot
execute unless entity @s[type=marker, tag=mtb.example-test_five] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:v0.1-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:v0.1-alpha/display, predicate=mtb:v0.1-alpha/match_id]
execute at @s run tp @s ^-0.5 ^ ^-0.5
execute rotated as @s run rotate @s ~90 ~
execute at @s rotated as @s run tp @s ^0.5 ^ ^0.5
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:example/test_five/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:example/test_five/outline/spawn_correct_outline
