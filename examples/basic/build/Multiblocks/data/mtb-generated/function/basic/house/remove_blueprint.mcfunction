execute unless function mtb-generated:basic/house/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
tag @s remove mtb.has_blueprint
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.basic-house, tag=mtb.blueprint, tag=!mtb.root]
scoreboard players set @s mtb_complete 0
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Hiding blueprint for house instance","color":"white"}]

