


# -------------------------------
#  Right Click Detection                            
# -------------------------------

execute if score @s coas_use matches 1 if predicate advanced:holding/schematic run function advanced:schematic/menu/input/click


# Reset the coas use so we can re-use it later
execute if score @s coas_use matches 1.. run scoreboard players reset @s coas_use

# -------------------------------
#  Sprint key detection                            
# -------------------------------

# Increase the score while holding the sprint key.
# when released, the score is -1 for one tick so we can also detect that
execute unless score @s sprint_use matches 0.. run scoreboard players set @s sprint_use 0
execute unless predicate advanced:sprint if score @s sprint_use matches 1.. run scoreboard players set @s sprint_use -1
execute if predicate advanced:sprint run scoreboard players add @s sprint_use 1

execute if predicate advanced:holding/schematic if score @s sprint_use matches 1 run function advanced:schematic/menu/input/sprint_press

# Sound effects
execute if predicate advanced:holding/schematic if score @s sprint_use matches 1 run playsound minecraft:block.crafter.craft master @s ~ ~ ~ 1 2
execute if predicate advanced:holding/schematic if score @s sprint_use matches -1 run playsound minecraft:block.crafter.fail master @a ~ ~ ~ 10 0