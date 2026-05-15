execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
$scoreboard players set #rot.target temp $(rotation)
execute unless score #rot.target temp matches 0 unless score #rot.target temp matches 90 unless score #rot.target temp matches 180 unless score #rot.target temp matches 270 run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Failed to set steam_engine rotation. Rotation must be one of 0, 90, 180 or 270","color":"red"}]
$execute if entity @s[tag=mtb.rot_$(rotation)] run return fail
tag @s remove mtb.rot_0
tag @s remove mtb.rot_90
tag @s remove mtb.rot_180
tag @s remove mtb.rot_270
$tag @s add mtb.rot_$(rotation)
$rotate @s $(rotation) 0
function mtb:v0.1.2-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id, tag=!mtb.root]
execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function mtb-generated:custom_block/steam_engine/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] rotated as @s run function mtb-generated:custom_block/steam_engine/outline/spawn_correct_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Modified rotation of steam_engine instance","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_edit
