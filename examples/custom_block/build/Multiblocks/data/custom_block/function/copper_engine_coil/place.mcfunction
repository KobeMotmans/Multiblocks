


# We have a max limit the block can move up
execute if entity @s[distance=10..] run return run kill @s

# Move the block upwards if this spot isn't air (yes this is not completely accurate placement, just shut tf up lol)
execute unless block ~ ~ ~ air positioned ~ ~1 ~ run return run function custom_block:copper_engine_coil/place


# ======= Actually place the block =======

# entities
execute align xyz run summon block_display ~ ~ ~ {Passengers:[{id:"minecraft:block_display",block_state:{Name:"minecraft:polished_blackstone",Properties:{}},transformation:[0.5000f,0.0000f,0.0000f,0.2500f,0.0000f,0.8125f,0.0000f,0.0625f,0.0000f,0.0000f,0.5000f,0.2500f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.0630f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.1875f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.3125f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.4375f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.5625f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:copper_block",Properties:{}},transformation:[0.7500f,0.0000f,0.0000f,0.1250f,0.0000f,0.0625f,0.0000f,0.6875f,0.0000f,0.0000f,0.7500f,0.1250f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:netherite_block",Properties:{}},transformation:[1.0000f,0.0000f,0.0000f,0.0000f,0.0000f,0.0625f,0.0000f,0.0020f,0.0000f,0.0000f,1.0000f,0.0000f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:cauldron",Properties:{}},transformation:[0.6250f,0.0000f,0.0000f,0.1875f,0.0000f,-0.1875f,-0.0000f,1.0000f,0.0000f,0.0000f,-0.6250f,0.8125f,0.0000f,0.0000f,0.0000f,1.0000f]},{id:"minecraft:block_display",block_state:{Name:"minecraft:cauldron",Properties:{}},transformation:[0.6250f,0.0000f,0.0000f,0.1875f,0.0000f,-0.1875f,-0.0000f,0.1875f,0.0000f,0.0000f,-0.6250f,0.8125f,0.0000f,0.0000f,0.0000f,1.0000f]}],Tags:[cb.copper_coil,smithed.block,smithed.entity,smithed.strict]}

# Sounds
playsound minecraft:block.copper.place block @a ~ ~ ~
playsound minecraft:block.lodestone.place block @a ~ ~ ~

# Physical block
setblock ~ ~ ~ minecraft:polished_blackstone_wall

# Kill the placement marker
execute if entity @s[type=marker,tag=copper_coil_placement] run kill @s