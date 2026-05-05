execute unless entity @s[type=marker, tag=mtb.example-test_two] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Must run this command as the marker","color":"red"}
function mtb:find_id
tag @s remove mtb.has_blueprint
kill @e[type=#mtb:display, predicate=mtb:match_id,tag=mtb.example-test_two, tag=mtb.blueprint]
