execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
tag @s remove mtb.has_blueprint
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.custom_block-steam_engine, tag=mtb.blueprint, tag=!mtb.root]
scoreboard players set @s mtb_complete 0
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Hiding blueprint for steam_engine instance","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_edit
