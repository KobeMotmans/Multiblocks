execute unless entity @s[tag=mtb.has_blueprint] run scoreboard players set #mtb_blueprint temp 1
execute if score #mtb_blueprint temp matches 1 run function mtb-generated:custom_block/steam_engine/place_blueprint/show_blueprint
function mtb:v0.1.2-alpha/find_id
execute as @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.custom_block-steam_engine, tag=mtb.blueprint] at @s run setblock ~ ~ ~ air
execute if score #mtb_blueprint temp matches 1 run function mtb-generated:custom_block/steam_engine/remove_blueprint
scoreboard players reset #mtb_blueprint temp
execute at @s run function custom_block:schematic/blueprint/on_clear_area
execute as @a at @s run function #mtb:update_multiblock
