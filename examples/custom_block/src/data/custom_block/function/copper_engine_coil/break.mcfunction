

# Sfx
playsound minecraft:block.copper.break block @a ~0.5 ~0.5 ~0.5
particle minecraft:block{block_state:"minecraft:copper_block"} ~0.5 ~0.5 ~0.5 0.35 0.35 0.35 0.35 20 force

# Kill the entities
execute on passengers run kill @s
kill @s