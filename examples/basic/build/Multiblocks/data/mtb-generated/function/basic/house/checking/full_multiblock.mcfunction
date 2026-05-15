execute store success score #cond_met temp run function mtb-generated:basic/house/checking/conditions
execute if score @s mtb_complete matches 251 unless score #cond_met temp matches 1 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: house almost completed: mtb built but conditions are not met","color":"gold"}
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 251 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: house was completed!","color":"green"}]
execute if score #cond_met temp matches 1 if score @s mtb_complete matches 251 unless entity @s[tag=mtb.completed] run function basic:on_complete
execute if score @s mtb_complete matches 251 run tag @s add mtb.completed
execute unless score @s mtb_complete matches 251 run tag @s remove mtb.completed
