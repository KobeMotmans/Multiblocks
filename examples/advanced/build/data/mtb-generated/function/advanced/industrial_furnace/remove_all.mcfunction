execute unless function mtb-generated:advanced/industrial_furnace/verify_marker run return fail
function mtb:v0.1.2-alpha/find_id
kill @e[predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.advanced-industrial_furnace]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Removed industrial_furnace instance","color":"white"}]
