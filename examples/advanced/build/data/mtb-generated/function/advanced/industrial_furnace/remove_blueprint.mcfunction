execute unless function mtb-generated:advanced/industrial_furnace/verify_marker run return fail
function mtb:v0.1.2-alpha/find_id
tag @s remove mtb.has_blueprint
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.advanced-industrial_furnace, tag=mtb.blueprint]
scoreboard players set @s mtb_complete 0
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Hiding blueprint for industrial_furnace instance","color":"white"}]
