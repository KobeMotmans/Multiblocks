playsound minecraft:entity.armadillo.brush master @s ~ ~ ~ 1 2
swing @s


# Reposition and creative place
execute unless entity @s[tag=blueprint_positioned] run scoreboard players set @s schematic.menu 0
execute unless entity @s[tag=blueprint_positioned] as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] run function custom_block:schematic/blueprint/edit_mode/init
execute unless entity @s[tag=blueprint_positioned] run tag @s add blueprint_positioned

execute if score @s schematic.menu matches 1 as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/build_structure

execute if score @s schematic.menu matches 1..2 run tag @s remove blueprint_positioned
execute if score @s schematic.menu matches 2 as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/blueprint/hide
execute if score @s schematic.menu matches 2 as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/outline/modify {args:{}}


# Nudge x
execute if score @s schematic.menu matches 3 if predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/decr_x
execute if score @s schematic.menu matches 3 unless predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/incr_x
# Nudge y
execute if score @s schematic.menu matches 4 if predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/decr_y
execute if score @s schematic.menu matches 4 unless predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/incr_y
# Nudge z
execute if score @s schematic.menu matches 5 if predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/decr_z
execute if score @s schematic.menu matches 5 unless predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/move/incr_z

# Rotate
execute if score @s schematic.menu matches 6 if predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/rotate/counter_clockwise
execute if score @s schematic.menu matches 6 unless predicate custom_block:sneak as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/rotate/clockwise

# Mirror
execute if score @s schematic.menu matches 7 as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] at @s run function #mtb-generated:custom_block/steam_engine/mirror

function custom_block:schematic/menu/build