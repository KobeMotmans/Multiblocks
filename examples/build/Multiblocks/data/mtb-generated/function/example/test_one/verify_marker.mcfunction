execute if entity @s[type=marker,tag=mtb.example-test_one] run return 1
execute unless entity @s[type=marker] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Error: failed to build structure. Please run the command as the multiblock root.","color":"red"}
execute unless entity @s[tag=mtb.example-test_one] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {"text":"[Debug]: Error: failed to build structure. Please run the correct function for this multiblock.","color":"red"}
return fail
