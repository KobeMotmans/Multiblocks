tp @s ^ ^2.5 ^2.0
execute if data storage mtb:temp {args: {mirrored: true}} run tag @s add mirrored
execute at @s run function mtb-generated:test_two/multiblock_init
