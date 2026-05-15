execute store success score #cond_met temp run function mtb-generated:advanced/industrial_furnace/checking/conditions
execute if score @s mtb_complete matches 37 unless score #cond_met temp matches 1 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: industrial_furnace almost completed: mtb built but conditions are not met","color":"gold"}
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 37 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: industrial_furnace was completed!","color":"green"}]
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 37 unless entity @s[tag=mtb.completed] run say industrial_furnace completed
execute if score @s mtb_complete matches 37 run tag @s add mtb.completed
execute unless score @s mtb_complete matches 37 run tag @s remove mtb.completed
