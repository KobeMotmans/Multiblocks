execute unless function mtb-generated:advanced/industrial_furnace/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
execute as @e[tag=mtb.advanced-industrial_furnace, predicate=mtb:v0.1.2-alpha/match_id] at @s run tp @s ~1 ~ ~
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Moving industrial_furnace instance +X","color":"white"}]

