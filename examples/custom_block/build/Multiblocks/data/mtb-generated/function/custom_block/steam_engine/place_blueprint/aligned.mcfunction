function mtb-generated:custom_block/steam_engine/place_blueprint/handle_rotation
execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.custom_block-steam_engine, tag=INIT, tag=mtb.root, distance=..0.1] if data storage mtb:temp {"args":{"mirrored":true}} run tag @s add mtb.mirrored
execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.custom_block-steam_engine, tag=INIT, tag=mtb.root, distance=..0.1] at @s rotated as @s run function mtb-generated:custom_block/steam_engine/place_blueprint/init_root
