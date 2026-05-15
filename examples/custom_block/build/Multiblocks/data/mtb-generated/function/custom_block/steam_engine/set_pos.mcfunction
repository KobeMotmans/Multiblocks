execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
execute align xyz run tp @s ~0.5 ~0.5 ~0.5
execute at @s run function mtb-generated:custom_block/steam_engine/place_blueprint/init_root
execute store result score #pos_x temp run data get entity @s Pos[0]
execute store result score #pos_y temp run data get entity @s Pos[1]
execute store result score #pos_z temp run data get entity @s Pos[2]
execute if score #pos_x temp = @s mtb_prev_x if score #pos_y temp = @s mtb_prev_y if score #pos_z temp = @s mtb_prev_z run return fail
scoreboard players operation @s mtb_prev_x = #pos_x temp
scoreboard players operation @s mtb_prev_y = #pos_y temp
scoreboard players operation @s mtb_prev_z = #pos_z temp
function mtb:v0.1.2-alpha/find_id
kill @e[tag=mtb.custom_block-steam_engine, predicate=mtb:v0.1.2-alpha/match_id, tag=!mtb.root,type=#mtb:v0.1.2-alpha/display]
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:custom_block/steam_engine/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:custom_block/steam_engine/outline/spawn_correct_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Repositioning steam_engine instance","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_edit
