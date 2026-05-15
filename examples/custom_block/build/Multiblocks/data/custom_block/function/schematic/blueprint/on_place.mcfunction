# This function runs from the on_place callback specified in the json file

# Give this multiblock the same ID as the player

# We summon the mtb in the player function here thus the on place runs per-player individually 
# This means that we can use the #search fake player to get the ID of the player
scoreboard players operation @s ID = #search ID