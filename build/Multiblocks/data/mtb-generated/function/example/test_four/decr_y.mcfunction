execute unless entity @s[type=marker, tag=mtb.example-test_four] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:find_id
execute as @e[tag=mtb.example-test_four, predicate=mtb:match_id] at @s run tp @s ~ ~-1 ~
