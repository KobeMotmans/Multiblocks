execute unless function mtb-generated:advanced/industrial_furnace/verify_marker run return fail
execute at @s positioned ^-1.0 ^-2.0 ^-1.0 run function mtb-generated:advanced/industrial_furnace/place_template
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: industrial_furnace instance built","color":"white"}]
