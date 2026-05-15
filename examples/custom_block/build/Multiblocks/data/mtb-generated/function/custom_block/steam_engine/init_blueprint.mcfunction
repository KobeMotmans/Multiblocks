data remove storage mtb:temp args
$data modify storage mtb:temp args set value $(args)
execute align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:custom_block/steam_engine/place_blueprint/aligned
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Summoned new steam_engine instance","color":"white"}]
