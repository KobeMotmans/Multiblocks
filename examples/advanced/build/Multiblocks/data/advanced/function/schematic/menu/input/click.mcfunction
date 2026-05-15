playsound minecraft:entity.armadillo.brush master @s ~ ~ ~ 1 2
swing @s


# Reposition and creative place
execute unless entity @s[tag=blueprint_positioned] run scoreboard players set @s schematic.menu 0
execute unless entity @s[tag=blueprint_positioned] as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] run function advanced:schematic/blueprint/edit_mode/init
execute unless entity @s[tag=blueprint_positioned] run tag @s add blueprint_positioned

execute if score @s schematic.menu matches 1 as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/build_structure

execute if score @s schematic.menu matches 1..2 run tag @s remove blueprint_positioned

# Nudge x
execute if score @s schematic.menu matches 3 if predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/decr_x
execute if score @s schematic.menu matches 3 unless predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/incr_x
# Nudge y
execute if score @s schematic.menu matches 4 if predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/decr_y
execute if score @s schematic.menu matches 4 unless predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/incr_y
# Nudge z
execute if score @s schematic.menu matches 5 if predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/decr_z
execute if score @s schematic.menu matches 5 unless predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/move/incr_z

# Rotate
execute if score @s schematic.menu matches 6 if predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/rotate/counter_clockwise
execute if score @s schematic.menu matches 6 unless predicate advanced:sneak as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/rotate/clockwise

# Mirror
execute if score @s schematic.menu matches 7 as @e[type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] at @s run function #mtb-generated:advanced/industrial_furnace/mirror

function advanced:schematic/menu/build