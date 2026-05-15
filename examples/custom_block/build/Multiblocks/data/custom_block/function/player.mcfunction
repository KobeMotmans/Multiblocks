
# Assign an id to this player
function advanced:player_id/assign_id

scoreboard players operation #search ID = @s ID

# -------------------------------
#  Blueprint placement                            
# -------------------------------

execute unless entity @s[tag=blueprint_positioned] if predicate custom_block:holding/schematic/steam_engine if entity @s[tag=!holding_schematic] run function #mtb-generated:custom_block/steam_engine/summon_instance {args:{}}
execute unless entity @s[tag=blueprint_positioned] unless predicate custom_block:holding/schematic/steam_engine if entity @s[tag=holding_schematic] \
    as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root,predicate=custom_block:match_search_id,limit=1] run function #mtb-generated:custom_block/steam_engine/remove_instance

execute unless entity @s[tag=blueprint_positioned] if predicate custom_block:holding/schematic/steam_engine anchored eyes run function custom_block:schematic/blueprint/place_mode/raycast

# -------------------------------
#  Schematic menu                            
# -------------------------------

# Update the menu when the player starts / stops holding the schematic
execute if predicate custom_block:holding/schematic/steam_engine if entity @s[tag=!holding_schematic] run function custom_block:schematic/menu/build
execute unless predicate custom_block:holding/schematic/steam_engine if entity @s[tag=holding_schematic] run title @s actionbar {"text": ""}

execute if predicate custom_block:holding/schematic/steam_engine run tag @s add holding_schematic
execute unless predicate custom_block:holding/schematic/steam_engine run tag @s remove holding_schematic

# Update the menu every 15 ticks when holding the schematic
execute if score #15 slow_tick matches 0 if predicate custom_block:holding/schematic/steam_engine run function custom_block:schematic/menu/build

# Handle menu input
function custom_block:schematic/menu/handle_input

# -------------------------------
#  Coil Placement                            
# -------------------------------

execute if score @s use_cod_egg matches 1.. as @e[type=marker,tag=copper_coil_placement] at @s run function custom_block:copper_engine_coil/place


# -------------------------------
#  Score resets                            
# -------------------------------
scoreboard players reset @s use_cod_egg