# This function displays the current state of the schematic menu to the screen

execute unless score @s schematic.menu matches 1.. run scoreboard players set @s schematic.menu 1


execute unless entity @s[tag=blueprint_positioned] run scoreboard players set @s schematic.menu 2


execute if score @s schematic.menu matches 1 run data modify storage advanced:schematic menu.creative_place set value {"text":" >Creative Place< ","color":"light_purple"}
execute unless score @s schematic.menu matches 1 run data modify storage advanced:schematic menu.creative_place set value {"text":"  Creative Place  ","color":"gray"}

execute if score @s schematic.menu matches 2 run data modify storage advanced:schematic menu.change_position set value {"text":" >Position< ","color":"aqua"}
execute unless score @s schematic.menu matches 2 run data modify storage advanced:schematic menu.change_position set value {"text":"  Position  ","color":"gray"}

execute if score @s schematic.menu matches 3 if predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_x set value {"text":" >Nudge X< ","color":"red"}
execute if score @s schematic.menu matches 3 unless predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_x set value {"text":" >Nudge X< ","color":"aqua"}
execute unless score @s schematic.menu matches 3 run data modify storage advanced:schematic menu.nudge_x set value {"text":"  Nudge X  ","color":"gray"}

execute if score @s schematic.menu matches 4 if predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_y set value {"text":" >Nudge Y< ","color":"red"}
execute if score @s schematic.menu matches 4 unless predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_y set value {"text":" >Nudge Y< ","color":"aqua"}
execute unless score @s schematic.menu matches 4 run data modify storage advanced:schematic menu.nudge_y set value {"text":"  Nudge Y  ","color":"gray"}

execute if score @s schematic.menu matches 5 if predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_z set value {"text":" >Nudge Z< ","color":"red"}
execute if score @s schematic.menu matches 5 unless predicate advanced:sneak run data modify storage advanced:schematic menu.nudge_z set value {"text":" >Nudge Z< ","color":"aqua"}
execute unless score @s schematic.menu matches 5 run data modify storage advanced:schematic menu.nudge_z set value {"text":"  Nudge Z  ","color":"gray"}

execute if score @s schematic.menu matches 6 if predicate advanced:sneak run data modify storage advanced:schematic menu.rotate set value {"text":" >Rotate< ","color":"red"}
execute if score @s schematic.menu matches 6 unless predicate advanced:sneak run data modify storage advanced:schematic menu.rotate set value {"text":" >Rotate< ","color":"aqua"}
execute unless score @s schematic.menu matches 6 run data modify storage advanced:schematic menu.rotate set value {"text":"  Rotate  ","color":"gray"}

execute if score @s schematic.menu matches 7 if predicate advanced:sneak run data modify storage advanced:schematic menu.mirror set value {"text":" >Mirror< ","color":"red"}
execute if score @s schematic.menu matches 7 unless predicate advanced:sneak run data modify storage advanced:schematic menu.mirror set value {"text":" >Mirror< ","color":"yellow"}
execute unless score @s schematic.menu matches 7 run data modify storage advanced:schematic menu.mirror set value {"text":"  Mirror  ","color":"gray"}


execute if entity @s[tag=blueprint_positioned] run title @s actionbar [ \
    {"text":"["},{"keybind":"key.sprint"},{"text":"] |"}, \
    {"nbt":"menu.creative_place","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.change_position","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.nudge_x","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.nudge_y","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.nudge_z","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.rotate","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"nbt":"menu.mirror","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"text":" ["},{"keybind":"key.use"},{"text":"]"} \
]

execute unless entity @s[tag=blueprint_positioned] run title @s actionbar [ \
    {"text":"["},{"keybind":"key.sprint"},{"text":"] |"}, \
    {"nbt":"menu.change_position","storage":"advanced:schematic","interpret":true},{"text":"|"}, \
    {"text":" ["},{"keybind":"key.use"},{"text":"]"} \
]