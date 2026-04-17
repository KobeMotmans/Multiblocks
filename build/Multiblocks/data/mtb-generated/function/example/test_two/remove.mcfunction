execute unless entity @s[type=marker, tag=example-test_two] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"Must run this command as the marker","color":"red"}
function mtb:find_id
kill @e[predicate=mtb:match_id,tag=example-test_two]
