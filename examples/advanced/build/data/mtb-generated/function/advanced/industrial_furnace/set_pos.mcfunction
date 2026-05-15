execute unless function mtb-generated:advanced/industrial_furnace/verify_marker run return fail
execute align xyz run tp @s ~0.5 ~0.5 ~0.5
execute at @s run function mtb-generated:advanced/industrial_furnace/place_blueprint/init_marker
execute store result score #pos_x temp run data get entity @s Pos[0]
execute store result score #pos_y temp run data get entity @s Pos[1]
execute store result score #pos_z temp run data get entity @s Pos[2]
execute if score #pos_x temp = @s mtb_prev_x if score #pos_y temp = @s mtb_prev_y if score #pos_z temp = @s mtb_prev_z run return fail
scoreboard players operation @s mtb_prev_x = #pos_x temp
scoreboard players operation @s mtb_prev_y = #pos_y temp
scoreboard players operation @s mtb_prev_z = #pos_z temp
function mtb:v0.1.2-alpha/find_id
kill @e[tag=mtb.advanced-industrial_furnace, predicate=mtb:v0.1.2-alpha/match_id,type=#mtb:v0.1.2-alpha/display]
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/outline/spawn_correct_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Repositioning industrial_furnace instance","color":"white"}]
