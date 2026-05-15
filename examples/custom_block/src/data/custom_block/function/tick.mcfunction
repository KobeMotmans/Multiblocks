
# -------------------------------
#  Handle slow ticking                            
# -------------------------------

scoreboard players add #15 slow_tick 1


execute if score #15 slow_tick matches 15 run scoreboard players set #15 slow_tick 0

# -------------------------------
#  Main code                            
# -------------------------------

# Run the player
execute as @a at @s run function custom_block:player

# Run the custom block
execute as @e[type=minecraft:block_display,tag=cb.copper_coil] at @s run function custom_block:copper_engine_coil/tick

# Run the completed multiblock
execute as @e[type=minecraft:block_display,tag=mtb.custom_block-steam_engine,tag=mtb.root] at @s run function custom_block:schematic/blueprint/completed/check

# Loop
schedule function custom_block:tick 1t replace