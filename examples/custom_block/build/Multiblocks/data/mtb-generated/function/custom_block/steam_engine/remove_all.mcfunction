execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
tag @s remove mtb.has_outline
tag @s remove mtb.has_blueprint
execute at @s run function custom_block:schematic/blueprint/on_edit
function mtb:v0.1.2-alpha/find_id
kill @e[predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.custom_block-steam_engine]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Removed steam_engine instance","color":"white"}]
