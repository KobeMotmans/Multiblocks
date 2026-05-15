execute if entity @s[tag=has_id] run return fail

execute unless score #max ID matches 0.. run scoreboard players set #max ID 0
scoreboard players operation @s ID = #max ID
scoreboard players add #max ID 1

tag @s add has_id