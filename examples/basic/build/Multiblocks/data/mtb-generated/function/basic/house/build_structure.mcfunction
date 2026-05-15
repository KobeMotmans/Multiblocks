execute unless function mtb-generated:basic/house/verify_marker run return fail
execute at @s positioned ^-3.0 ^-3.5 ^-4.0 run function mtb-generated:basic/house/place_template
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: house instance built","color":"white"}]
