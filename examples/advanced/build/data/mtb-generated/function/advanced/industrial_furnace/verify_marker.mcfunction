execute if entity @s[type=marker,tag=mtb.advanced-industrial_furnace] run return 1
execute unless entity @s[type=marker] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Error: failed to interact with multiblock. Please run the command as the multiblock root.","color":"red"}
execute if entity @s[type=marker] unless entity @s[tag=mtb.advanced-industrial_furnace] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Error: to interact with multiblock. Please run the correct function for this multiblock.","color":"red"}
return fail
