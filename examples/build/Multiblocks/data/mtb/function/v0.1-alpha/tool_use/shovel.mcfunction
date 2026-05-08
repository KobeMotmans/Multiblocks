advancement revoke @s only mtb:v0.1-alpha/tool_use/shovel
scoreboard players set @s mtb_wood_shovel 0
scoreboard players set @s mtb_stone_shovel 0
scoreboard players set @s mtb_gold_shovel 0
scoreboard players set @s mtb_copper_shovel 0
scoreboard players set @s mtb_iron_shovel 0
scoreboard players set @s mtb_diamond_shovel 0
scoreboard players set @s mtb_netherite_shovel 0
execute at @s run function #mtb:update_multiblock
