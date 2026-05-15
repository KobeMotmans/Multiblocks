tp @s ^0.0 ^2.0 ^2.0
tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:v0.1.2-alpha/assign_id
scoreboard players set @s mtb_complete 0
function advanced:schematic/blueprint/on_place
