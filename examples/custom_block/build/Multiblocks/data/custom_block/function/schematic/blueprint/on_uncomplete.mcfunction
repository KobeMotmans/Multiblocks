# This function runs from the on_uncomplete callback specified in the json file


playsound minecraft:block.respawn_anchor.set_spawn master @a ~ ~ ~ 1 2
particle minecraft:dust{color:[0.8, 0.0, 0.0],scale:1} ~ ~ ~ 1.1 0.9 0.7 0 100
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 1 1.4

function #mtb-generated:custom_block/steam_engine/outline/show