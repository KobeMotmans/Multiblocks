execute as @a at @s run function #mtb:update_multiblock
schedule function mtb:v0.1-alpha/slow_tick 10t replace
advancement revoke @s only mtb:v0.1-alpha/events/place_block
