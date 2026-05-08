tp @s ^0.0 ^1.0 ^2.5
tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
scoreboard players set @s mtb_complete 0
