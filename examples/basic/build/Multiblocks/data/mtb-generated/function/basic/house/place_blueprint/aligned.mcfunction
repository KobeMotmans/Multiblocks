function mtb-generated:basic/house/place_blueprint/handle_rotation
execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.basic-house, tag=INIT, tag=mtb.root, distance=..0.1] if data storage mtb:temp {"args":{"mirrored":true}} run tag @s add mtb.mirrored
execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.basic-house, tag=INIT, tag=mtb.root, distance=..0.1] at @s rotated as @s run function mtb-generated:basic/house/place_blueprint/init_root
