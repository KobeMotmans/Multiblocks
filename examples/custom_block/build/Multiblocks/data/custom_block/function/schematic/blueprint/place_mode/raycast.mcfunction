
# Run the raycast when the current block is air
execute if block ~ ~ ~ air positioned ^ ^ ^0.1 if entity @s[distance=..15] run return run function custom_block:schematic/blueprint/place_mode/raycast


# Yay we've found a block, move the blueprint there

execute if entity @s[y_rotation=-45..45] run scoreboard players set #rot.target temp 0
execute if entity @s[y_rotation=45..135] run scoreboard players set #rot.target temp 90
execute if entity @s[y_rotation=135..225] run scoreboard players set #rot.target temp 180
execute if entity @s[y_rotation=225..315] run scoreboard players set #rot.target temp 270
execute align xyz positioned ~0.5 ~1.5 ~0.5 as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] run function custom_block:schematic/blueprint/place_mode/modify_blueprint