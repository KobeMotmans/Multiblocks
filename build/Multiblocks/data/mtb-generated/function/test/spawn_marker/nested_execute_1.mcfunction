tp @s ^ ^2.0 ^3.0
execute if data storage mtb:temp {args: {mirrored: true}} run tag @s add mirrored
execute at @s run function mtb-generated:test/multiblock_init
