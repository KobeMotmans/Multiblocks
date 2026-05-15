execute if data storage mtb:temp {"args":{"rotation": 180}} run return run summon minecraft:block_display ~ ~ ~ {Rotation:[180f,0f], Tags:[mtb.basic-house,"INIT",mtb.rot_180,mtb.root]}
execute if data storage mtb:temp {"args":{"rotation": 270}} run return run summon minecraft:block_display ~ ~ ~ {Rotation:[270f,0f], Tags:[mtb.basic-house,"INIT",mtb.rot_270,mtb.root]}
execute if data storage mtb:temp {"args":{"rotation": 90}} run return run summon minecraft:block_display ~ ~ ~ {Rotation:[90f,0f], Tags:[mtb.basic-house,"INIT",mtb.rot_90,mtb.root]}
summon minecraft:block_display ~ ~ ~ {Rotation:[0f,0f], Tags:[mtb.basic-house,"INIT",mtb.rot_0,mtb.root]}
