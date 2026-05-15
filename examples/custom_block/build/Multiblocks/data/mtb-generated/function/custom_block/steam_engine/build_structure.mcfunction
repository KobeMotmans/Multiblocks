execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
execute at @s positioned ^-1.0 ^-1.5 ^-2.0 run function mtb-generated:custom_block/steam_engine/place_template
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: steam_engine instance built","color":"white"}]
execute at @s run function custom_block:schematic/blueprint/on_creative_place
