data remove storage mtb:temp args
$data modify storage mtb:temp args set value $(args)
execute align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:advanced/industrial_furnace/place_blueprint/aligned
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Summoned new industrial_furnace instance","color":"white"}]
