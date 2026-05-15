execute store success score #cond_met temp run function mtb-generated:custom_block/steam_engine/checking/conditions
execute if score @s mtb_complete matches 36 unless score #cond_met temp matches 1 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: steam_engine almost completed: mtb built but conditions are not met","color":"gold"}
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 36 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: steam_engine was completed!","color":"green"}]
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 36 unless entity @s[tag=mtb.completed] run function custom_block:schematic/blueprint/on_complete
execute unless score #cond_met temp matches 1 if score @s mtb_complete matches 36 if entity @s[tag=mtb.completed] run function custom_block:schematic/blueprint/on_uncomplete
execute if score @s mtb_complete matches 36 if score #cond_met temp matches 1 run tag @s add mtb.completed
execute unless score @s mtb_complete matches 36 run tag @s remove mtb.completed
execute unless score #cond_met temp matches 1 run tag @s remove mtb.completed
