# Runs when the player presses their sprint key

scoreboard players add @s schematic.menu 1
execute if score @s schematic.menu matches 8.. run scoreboard players set @s schematic.menu 1

function custom_block:schematic/menu/build