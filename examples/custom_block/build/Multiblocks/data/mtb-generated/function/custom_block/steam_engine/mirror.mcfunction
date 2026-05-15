execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
function mtb:v0.1.2-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id, tag=!mtb.root]
execute as @s at @s rotated as @s run function mtb-generated:custom_block/steam_engine/mirror_nested
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Mirrored steam_engine instance","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_edit
