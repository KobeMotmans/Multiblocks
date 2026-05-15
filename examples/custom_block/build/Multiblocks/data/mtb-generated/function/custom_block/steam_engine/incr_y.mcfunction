execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
execute as @e[tag=mtb.custom_block-steam_engine, predicate=mtb:v0.1.2-alpha/match_id] at @s run tp @s ~ ~1 ~
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Moving steam_engine instance +Y","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_edit
