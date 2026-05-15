execute unless entity @s[tag=mtb.has_blueprint] run scoreboard players set #mtb_blueprint temp 1
execute if score #mtb_blueprint temp matches 1 run function mtb-generated:basic/house/place_blueprint/show_blueprint
function mtb:v0.1.2-alpha/find_id
execute as @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id,tag=mtb.basic-house, tag=mtb.blueprint] at @s run setblock ~ ~ ~ air
execute if score #mtb_blueprint temp matches 1 run function mtb-generated:basic/house/remove_blueprint
scoreboard players reset #mtb_blueprint temp

execute as @a at @s run function #mtb:update_multiblock
