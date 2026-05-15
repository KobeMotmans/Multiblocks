execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
kill @e[type=block_display,tag=mtb.outline,predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.custom_block-steam_engine, tag=!mtb.root]
tag @s remove mtb.has_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Hiding outline for steam_engine instance","color":"white"}]
