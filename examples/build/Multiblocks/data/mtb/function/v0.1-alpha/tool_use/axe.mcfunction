advancement revoke @s only mtb:v0.1-alpha/tool_use/axe
scoreboard players set @s mtb_wood_axe 0
scoreboard players set @s mtb_stone_axe 0
scoreboard players set @s mtb_gold_axe 0
scoreboard players set @s mtb_copper_axe 0
scoreboard players set @s mtb_iron_axe 0
scoreboard players set @s mtb_diamond_axe 0
scoreboard players set @s mtb_netherite_axe 0
execute at @s run function #mtb:update_multiblock
