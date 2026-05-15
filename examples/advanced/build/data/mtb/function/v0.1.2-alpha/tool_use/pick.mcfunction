advancement revoke @s only mtb:v0.1.2-alpha/tool_use/pick
scoreboard players set @s mtb_wood_pick 0
scoreboard players set @s mtb_stone_pick 0
scoreboard players set @s mtb_gold_pick 0
scoreboard players set @s mtb_copper_pick 0
scoreboard players set @s mtb_iron_pick 0
scoreboard players set @s mtb_diamond_pick 0
scoreboard players set @s mtb_netherite_pick 0
execute at @s run function #mtb:update_multiblock
