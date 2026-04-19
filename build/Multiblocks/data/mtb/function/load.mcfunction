execute store result score #mtb.debug_enabled temp if entity @a[tag=mtb.debug]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text": "[Server]: Multiblocks v0.1-alpha loaded successfully","color":"green"}]
scoreboard objectives add mtb_complete dummy
scoreboard objectives add mtb_prev_state dummy
scoreboard objectives add mtb_id dummy
scoreboard objectives add mtb_wood_pick used:wooden_pickaxe
scoreboard objectives add mtb_stone_pick used:stone_pickaxe
scoreboard objectives add mtb_gold_pick used:golden_pickaxe
function mtb:run_command {"command":"scoreboard objectives add mtb_copper_pick used:copper_pickaxe"}
scoreboard objectives add mtb_iron_pick used:iron_pickaxe
scoreboard objectives add mtb_diamond_pick used:diamond_pickaxe
scoreboard objectives add mtb_netherite_pick used:netherite_pickaxe
scoreboard objectives add mtb_wood_axe used:wooden_axe
scoreboard objectives add mtb_stone_axe used:stone_axe
scoreboard objectives add mtb_gold_axe used:golden_axe
function mtb:run_command {"command":"scoreboard objectives add mtb_copper_axe used:copper_axe"}
scoreboard objectives add mtb_iron_axe used:iron_axe
scoreboard objectives add mtb_diamond_axe used:diamond_axe
scoreboard objectives add mtb_netherite_axe used:netherite_axe
scoreboard objectives add mtb_wood_shovel used:wooden_shovel
scoreboard objectives add mtb_stone_shovel used:stone_shovel
scoreboard objectives add mtb_gold_shovel used:golden_shovel
function mtb:run_command {"command":"scoreboard objectives add mtb_copper_shovel used:copper_shovel"}
scoreboard objectives add mtb_iron_shovel used:iron_shovel
scoreboard objectives add mtb_diamond_shovel used:diamond_shovel
scoreboard objectives add mtb_netherite_shovel used:netherite_shovel
scoreboard objectives add mtb_wood_hoe used:wooden_hoe
scoreboard objectives add mtb_stone_hoe used:stone_hoe
scoreboard objectives add mtb_gold_hoe used:golden_hoe
function mtb:run_command {"command":"scoreboard objectives add mtb_copper_hoe used:copper_hoe"}
scoreboard objectives add mtb_iron_hoe used:iron_hoe
scoreboard objectives add mtb_diamond_hoe used:diamond_hoe
scoreboard objectives add mtb_netherite_hoe used:netherite_hoe
scoreboard objectives add temp dummy
function #mtb:init_storage
schedule function mtb:slow_tic 1t replace
