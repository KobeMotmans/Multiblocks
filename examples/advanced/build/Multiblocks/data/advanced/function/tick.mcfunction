
# -------------------------------
#  Handle slow ticking                            
# -------------------------------

scoreboard players add #15 slow_tick 1


execute if score #15 slow_tick matches 15 run scoreboard players set #15 slow_tick 0

# -------------------------------
#  Main functions                            
# -------------------------------

execute as @a at @s run function advanced:player


# Re-run this function next tick
schedule function advanced:tick 1t replace