execute unless function mtb-generated:basic/house/verify_marker run return fail
function mtb:v0.1.2-alpha/find_id
kill @e[type=block_display,tag=mtb.outline,predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.basic-house]
tag @s remove mtb.has_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Hiding outline for house instance","color":"white"}]
