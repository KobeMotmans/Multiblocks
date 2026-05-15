
scoreboard players operation #search ID = @s ID

# -------------------------------
#  Blueprint placement                            
# -------------------------------

execute unless entity @s[tag=blueprint_positioned] if predicate advanced:holding/schematic if entity @s[tag=!holding_schematic] run function #mtb-generated:advanced/industrial_furnace/summon_instance {args:{}}
execute unless entity @s[tag=blueprint_positioned] unless predicate advanced:holding/schematic if entity @s[tag=holding_schematic] \
    as @e[type=marker,tag=mtb.advanced-industrial_furnace,tag=mtb.root,predicate=advanced:match_search_id,limit=1] run function #mtb-generated:advanced/industrial_furnace/remove_instance

execute unless entity @s[tag=blueprint_positioned] if predicate advanced:holding/schematic anchored eyes run function advanced:schematic/blueprint/place_mode/raycast

# -------------------------------
#  Schematic menu                            
# -------------------------------

# Update the menu when the player starts / stops holding the schematic
execute if predicate advanced:holding/schematic if entity @s[tag=!holding_schematic] run function advanced:schematic/menu/build
execute unless predicate advanced:holding/schematic if entity @s[tag=holding_schematic] run title @s actionbar {"text": ""}

execute if predicate advanced:holding/schematic run tag @s add holding_schematic
execute unless predicate advanced:holding/schematic run tag @s remove holding_schematic

# Update the menu every 15 ticks when holding the schematic
execute if score #15 slow_tick matches 0 if predicate advanced:holding/schematic run function advanced:schematic/menu/build


# Handle menu input
function advanced:schematic/menu/handle_input