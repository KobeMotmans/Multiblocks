execute as @a at @s run function #mtb:players
schedule function mtb:slow_tick 10t replace
advancement revoke @s only mtb:events/place_block
